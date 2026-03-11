from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from WhenInRome.forms import UserForm, UserProfileForm
from WhenInRome.models import UserProfile

def index(request):
    return HttpResponse("When In Rome Index <a href='/wheninrome/about'>About</a>")

def about(request):
    return HttpResponse("When In Rome About <a href='/wheninrome/'>Index</a>")

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'WhenInRome/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('/wheninrome/')
            else:
                messages.error(request, 'Your account has been disabled.')
                return render(request, 'WhenInRome/login.html')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'WhenInRome/login.html')
    else:
        return render(request, 'WhenInRome/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/wheninrome/')

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request, 'WhenInRome/profile.html', {
        'user_profile': user_profile,
    })