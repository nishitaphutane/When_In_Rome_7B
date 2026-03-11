import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from WhenInRome.forms import UserForm, UserProfileForm
from WhenInRome.models import UserProfile
from WhenInRome.models import City
from WhenInRome.models import Recommendation

def index(request):
    category_list=City.objects.order_by('name').values()
    return render(request, 'wheninrome/city.html') # will update once templates are made so we can access our webapp

def about(request):
    context_dict = {}
    print(request.method)
    print(request.user)
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'wheninrome/about.html', context=context_dict)
    return response

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        city = City.objects.get(slug=category_name_slug)
        recommendations = Recommendation.objects.filter(city=city)
        context_dict['recommendations'] = recommendations
        context_dict['city'] = city
    except City.DoesNotExist:
        context_dict['city'] = None
        context_dict['recommendations'] = None
    return render(request, 'wheninrome/category.html', context=context_dict)

@login_required
def add_recommendation(request):
    # Will do once ReccomendationForm method is made in forms
    pass

@login_required
def add_city(request):
    pass

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

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits
