from django.contrib import admin
from django.urls import path
from django.urls import include
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'WhenInRome/base.html')

def about(request):
    return render(request, 'WhenInRome/about.html')
