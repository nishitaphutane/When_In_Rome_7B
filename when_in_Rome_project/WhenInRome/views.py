from django.contrib import admin
from django.urls import path
from django.urls import include
from django.http import HttpResponse

def index(request):
    return HttpResponse("When In Rome")
