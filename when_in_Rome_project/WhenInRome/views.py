import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'WhenInRome/base.html')

def about(request):
    return render(request, 'WhenInRome/about.html')
