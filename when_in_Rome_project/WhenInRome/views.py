import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from WhenInRome.models import Category, Page
def index(request):
    category_list = Category.objects.all()
    context_dict = {'categories' : category_list}
    return render(request, 'WhenInRome/index.html', context=context_dict)

def about(request):
    return render(request, 'WhenInRome/about.html')
def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'WhenInRome/category.html', context=context_dict)
    