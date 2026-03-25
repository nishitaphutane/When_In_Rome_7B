import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'when_in_Rome_project.settings')
import django
django.setup()
from WhenInRome.models import Category, Page

def populate():
    python_pages = [
        {'title': 'Kelvingrove Art Gallery', 'url': '', 'views': 50, 'location': 'Argyle St, West End', 'img': 'kelvingrove.jpg'},
        {'title': 'Glasgow Cathedral', 'url': '...', 'views': 30, 'location': 'Castle St, Townhead', 'img': 'cathedral.jpg'},
        {} ]
    django_pages = [
        {'title': 'Paesano Pizza', 'url': '...', 'views': 100, 'location': 'Miller St / Great Western Rd', 'img': 'paesano.jpg'},
        {'title': 'Mother India', 'url': '...', 'views': 80, 'location': 'West End', 'img': 'mother_india.jpg'},
        {} ]
    other_pages = [
        {'title': 'Buchanan Bus Station', 'url': '...', 'views': 20, 'location': 'City Centre', 'img': 'buchanan.jpg'},
        {'title': 'St Enoch Subway', 'url': '...', 'views': 45, 'location': 'St Enoch Square', 'img': 'stenoch.jpg'} ]
    cats = {'Landmarks': {'pages': python_pages, 'views' : 128, 'likes' : 64, 'image': 'Landmarks.png'},
            'Food': {'pages': django_pages, 'views' : 64, 'likes' : 32, 'image': 'Food.jpg'},
            'Transportation': {'pages': other_pages, 'views' : 32, 'likes' : 16, 'image': 'Transportation.jpg'} }
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'], image=cat_data['image'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0, location='', image=''):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.location = location
    p.save()
    return p

def add_cat(name, views=0, likes=0, image='default.jpg'):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.image_name=image
    c.save()
    return c

if __name__ == '__main__':
    print('Starting When In Rome population script...')
    populate()