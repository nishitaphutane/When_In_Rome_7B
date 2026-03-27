import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'when_in_Rome_project.settings')

import django
django.setup()

import random
from django.contrib.auth.models import User
from WhenInRome.models import City, Recommendation, UserProfile, Review, Upvote

def populate():
    print(" - Creating Users and Profiles...")
    users_data = [
        {'username': 'johnsmith', 'password': 'test123', 'email': 'johnsmith@example.com'},
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
                {'title': 'Botanic Gardens', 'description': 'Stunning glasshouses and riverside walks.', 'location': '730 Great Western Rd', 'image': 'BotanicGardens.png'},
                {'title': 'Pollock Park', 'description': 'Large scenic park with Highland cows.', 'location': '2060 Pollokshaws Rd', 'image': 'PollockPark.png'},
                {'title': 'University of Glasgow', 'description': 'Historic campus with Hogwarts vibes.', 'location': 'University Ave', 'image': 'UniofGlasgow.png'},
                {'title': 'Kelvingrove Art Gallery', 'description': 'Art and museum', 'location': 'Argyle St', 'image': 'KelvingroveMuseum.png'},
            ]
        },

        'Food': {
            'country': 'Scotland',
            'description': 'The best eats in Glasgow.',
            'image': 'page_images/Food.jpg',
            'recommendations': [
                {'title': 'Cafe Wanders', 'description': 'Cosy spot for brunch and coffee.', 'location': '8 Crosshill Rd', 'image': 'CafeWanders.png'},
                {'title': 'Hinba', 'description': 'Specialty coffee roasters from the Hebrides.', 'location': '721 Dumbarton Rd', 'image': 'Hinba.png'},
                {'title': 'Little Vietnam', 'description': 'Authentic Pho and Vietnamese street food.', 'location': '42 Station Rd', 'image': 'LittleVietnam.png'},
                {'title': 'Santa Lucia', 'description': 'Award-winning Italian pasta and hospitality.', 'location': 'Merchant City', 'image': 'SantaLucia.png'},
                {'title': 'Paesano Pizza', 'description': 'Best Neapolitan pizza', 'location': 'Miller St', 'image': 'PaesanoPizza.png'},
                {'title': 'Mother India', 'description': 'Famous tapas-style curry', 'location': 'West End', 'image': 'MotherIndia.png'},
            ]
        },
        'Transportation': {
            'country': 'Scotland',
            'description': 'Getting around the city with ease.',
            'image': 'page_images/Transportation.jpg',
            'recommendations': [
                {'title': 'Tour Bus', 'description': 'The best way to see all the sights in one go.', 'location': 'George Square', 'image': 'TourBus.png'},
                {'title': 'Clockwork Orange', 'description': 'The iconic Glasgow Subway system.', 'location': 'Inner & Outer Circles', 'image': 'ClockworkOrange.png'},
                {'title': 'Glasgow Central', 'description': 'The stunning Victorian main railway station.', 'location': 'Gordon St', 'image': 'GlasgowCentral.png'},
                {'title': 'Buchanan Bus Station', 'description': 'Main bus hub', 'location': 'City Centre', 'image': 'BuchananBusStation.png'},
            ]
        }
    }

    print("- Creating Cities and Recommendations...")
    for city_name, city_info in cities_data.items():
        c = add_city(city_name, city_info['country'], city_info['description'], city_info['image'])

        for rec in city_info['recommendations']:
            author = random.choice(users)
            r = add_recommendation(c, author, rec['title'], rec['description'], rec['location'], rec.get('image'))

            add_review(r, random.choice(users), rating=5, comment="Amazing place!")
            add_review(r, random.choice(users), rating=4, comment="Really enjoyed it.")

            for u in users:
                if random.random() > 0.5:
                    add_upvote(r, u)
            
    print(" - Setting up followers...")
    for user in users:
        potential_followers = [u for u in users if u != user]
        if potential_followers:
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

def add_recommendation(city, user, title, description, location, image=None):
    r, created = Recommendation.objects.get_or_create(
        city=city,
        title=title,
        defaults={'user': user, 'description': description, 'location': location, 'image': image}
    )
    if not created:
        r.description = description
        r.location = location
        if image:
            r.image = image
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
    profile, created = UserProfile.objects.get_or_create(user=user)
    for follower in followers:
        profile.followers.add(follower)
    profile.save()
    return profile

if __name__ == '__main__':
    print('Starting When In Rome population script...')
    populate()