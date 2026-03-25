import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'when_in_Rome_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from WhenInRome.models import City, Recommendation, UserProfile, Review, Upvote

import random

def populate():
    user = add_user('johnsmith', 'test123', 'johnsmith@example.com')
    add_user_profile(user)

    cats = {
        'Landmarks': {'country': 'Scotland',
            'image': 'city_images/Landmarks.png',
            'pages': [
                {'title': 'Kelvingrove Art Gallery', 'location': 'Argyle St, West End'},
                {'title': 'Glasgow Cathedral', 'location': 'Castle St, Townhead'},
            ]
        },
        'Food' : {'country': 'Scotland',
            'image': 'city_images/Food.jpg',
            'pages': [
                {'title': 'Paesano Pizza', 'location': 'Miller St'},
                {'title': 'Mother India', 'location': 'West End'},
            ]
        },
        'Transportation': {'country': 'Scotland',
            'image': 'city_images/Transportation.jpg',
            'pages': [
                {'title': 'Buchanan Bus Station', 'location': 'City Centre'},
                {'title': 'St Enoch Subway', 'location': 'St Enoch Square'},
            ]
        },
    }

    
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'], image=cat_data['image'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])
    users_data = [
        {'username': 'johnsmith', 'password': 'test123', 'email': 'johnsmith@example.com'},
        {'username': 'rachelgarcia', 'password': 'test123', 'email': 'rachelgarcia@example.com'},
        {'username': 'stevenwong', 'password': 'test123', 'email': 'stevenwong@example.com'},
        {'username': 'oliviawilson', 'password': 'test123', 'email': 'oliviawilson@example.com'},
        {'username': 'christaylor', 'password': 'test123', 'email': 'christaylor@example.com'},
        {'username': 'jamesstewart', 'password': 'test123', 'email': 'jamesstewart@example.com'},
    ]

    users = []
    for u in users_data:
        user = add_user(u['username'], u['password'],u['email'])
        add_user_profile(user)
        users.append(user)
    
    for user in users:
        potential_followers = [u for u in users if u != user]
        followers = random.sample(potential_followers, k=random.randint(1, len(potential_followers)))
        add_followers(user, followers)

def add_page(cat, title, url, views=0, location='', image=''):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.location = location
    p.save()
    return p

def add_cat(name, views=0, likes=0, image='default.jpg'):
    c = City.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.image_name=image

    cities_data = {
        'Glasgow': {
            'country': 'Scotland',
            'description': 'A vibrant cultural city',
            'recommendations': [
                {'title': 'Kelvingrove Art Gallery', 'description': 'Art and museum', 'location': 'Kelvingrove'},
                {'title': 'Glasgow Cathedral', 'description': 'Historic cathedral', 'location': 'Cathedral Square'},
            ]
        },
        'Edinburgh': {
            'country': 'Scotland',
            'description': 'Historic capital city',
            'recommendations': [
                {'title': 'Edinburgh Castle', 'description': 'Famous fortress', 'location': 'Castle Rock'},
                {'title': 'Arthur’s Seat', 'description': 'Great hike and views', 'location': 'Holyrood Park'},
            ]
        }
    }

    for city_name, city_data in cities_data.items():
        c = add_city(city_name, city_data['country'], city_data['description'])

        for rec in city_data['recommendations']:
            r = add_recommendation(
                city=c,
                user=users[0],
                title=rec['title'],
                description=rec['description'],
                location=rec['location']
            )

            add_review(r, users[1], rating=5, comment="Amazing!")
            add_review(r, users[2], rating=4, comment="Really good!")

            for user in users:
                if random.random() > 0.5:
                    add_upvote(r, user)

    for c in City.objects.all():
        for r in Recommendation.objects.filter(city=c):
            print(f'- {c}: {r}')


def add_user(username, password, email =''):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
    user.email = email
    user.save()
    return user


def add_user_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.bio = f"Hi, I'm {user.username}"
    profile.save()
    return profile


def add_city(name, country, description):
    c, created = City.objects.get_or_create(name=name)
    c.country = country
    c.description = description
    c.save()
    return c


def add_recommendation(city, user, title, description, location):
    r, created = Recommendation.objects.get_or_create(city=city, title=title, user=user)
    r.description = description
    r.location = location
    r.save()
    return r


def add_review(recommendation, user, rating, comment):
    review, created = Review.objects.get_or_create(recommendation=recommendation,user=user,defaults={'rating': rating,'comment': comment})

    if not created:
        review.rating = rating
        review.comment = comment
        review.save()

    return review


def add_upvote(recommendation, user):
    upvote, created = Upvote.objects.get_or_create(
        recommendation=recommendation,
        user=user
    )
    return upvote

def add_followers(user, followers):
    profile = UserProfile.objects.get(user=user)
    for follower in followers:
        profile.followers.add(follower)
    profile.save()
    return profile

if __name__ == '__main__':
    print('Starting When In Rome population script...')
    populate()