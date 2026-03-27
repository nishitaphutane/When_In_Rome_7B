import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'when_in_Rome_project.settings')

import django
django.setup()

import random
from django.contrib.auth.models import User
from WhenInRome.models import City, Recommendation, UserProfile, Review, Upvote


def populate():
    print(" - Creating Users and Profiles...")
    users_data = [{'username': 'johnsmith', 'password': 'test123', 'email': 'johnsmith@example.com'},
        {'username': 'rachelgarcia', 'password': 'test123', 'email': 'rachelgarcia@example.com'},
        {'username': 'stevenwong', 'password': 'test123', 'email': 'stevenwong@example.com'},
        {'username': 'oliviawilson', 'password': 'test123', 'email': 'oliviawilson@example.com'},
    ]

    users = []
    for u in users_data:
        user = add_user(u['username'], u['password'], u['email'])
        add_user_profile(user)
        users.append(user)

    cities_data = {
        'Landmarks': {
            'country': 'Scotland',
            'description': 'The historical heart of the city.',
            'image': 'page_images/Landmarks.jpg',
            'recommendations': [
                {'title': 'Kelvingrove Art Gallery', 'description': 'Art and museum', 'location': 'Argyle St'},
                {'title': 'Glasgow Cathedral', 'description': 'Historic medieval cathedral', 'location': 'Castle St'},
            ]
        },
        'Food': {
            'country': 'Scotland',
            'description': 'The best eats in Glasgow.',
            'image': 'page_images/Food.jpg',
            'recommendations': [
                {'title': 'Paesano Pizza', 'description': 'Best Neapolitan pizza', 'location': 'Miller St'},
                {'title': 'Mother India', 'description': 'Famous tapas-style curry', 'location': 'West End'},
            ]
        },
        'Transportation': {
            'country': 'Scotland',
            'description': 'Getting around the city with ease.',
            'image': 'page_images/Transportation.jpg',
            'recommendations': [
                {'title': 'Buchanan Bus Station', 'description': 'Main bus hub', 'location': 'City Centre'},
                {'title': 'St Enoch Subway', 'description': 'The Clockwork Orange', 'location': 'St Enoch Square'},
            ]
        }
    }


    print("- Creating Cities and Recommendations...")
    for city_name, city_info in cities_data.items():
        c = add_city(city_name, city_info['country'], city_info['description'], city_info['image'])

        for rec in city_info['recommendations']:
            author = random.choice(users)
            r = add_recommendation(c, author, rec['title'], rec['description'], rec['location'])

            add_review(r, random.choice(users), rating=5, comment="Amazing place!")
            add_review(r, random.choice(users), rating=4, comment="Really enjoyed it.")

            for u in users:
                if random.random() > 0.5:
                    add_upvote(r, u)
            
        print(" - Setting up followers...")
        for user in users:
            potential_followers = [u for u in users if u != user]
            followers = random.sample(potential_followers, k=random.randint(1, len(potential_followers)))
            add_followers(user, followers)
        print("Success: Database populated!")


def add_user(username, password, email=''):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
    user.email = email
    user.save()
    return user

def add_user_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.bio = f"Hi, I'm {user.username}, a travel enthusiast!"
    profile.save()
    return profile 

def add_city(name, country, description, image):
    c, created = City.objects.get_or_create(name=name)
    c.country = country
    c.description = description
    c.image = image
    c.save()
    return c

def add_recommendation(city, user, title, description, location):
    r, created = Recommendation.objects.get_or_create(
        city=city,
        title=title,
        user=user,
        defaults={'description': description, 'location': location}
    )
    if not created:
        r.description = description
        r.location = location
        r.save()
    return r
def add_review(recommendation, user, rating, comment):
    review, created = Review.objects.get_or_create(
        recommendation=recommendation,
        user=user,
        defaults={'rating': rating, 'comment': comment}
    )
    return review

def add_upvote(recommendation, user):
    upvote, created = Upvote.objects.get_or_create(recommendation=recommendation, user=user)
    return upvote

def add_followers(user, followers):
    profile = UserProfile.objects.get_or_create(user=user)[0]
    for follower in followers:
        profile.followers.add(follower)
    profile.save()
    return profile

if __name__ == '__main__':
    print('Starting When In Rome population script...')
    populate()
