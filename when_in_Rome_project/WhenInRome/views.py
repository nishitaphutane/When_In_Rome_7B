from django.contrib import admin
from django.urls import path
from django.urls import include
from django.http import HttpResponse

def index(request):
    return HttpResponse("When In Rome Index <a href='/wheninrome/about'>About</a>")

def about(request):
    return HttpResponse("When In Rome About <a href='/wheninrome/'>Index</a>")
