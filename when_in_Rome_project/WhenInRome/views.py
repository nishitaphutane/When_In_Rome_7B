import datetime
from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from WhenInRome.forms import UserForm, UserProfileForm
from WhenInRome.models import Category, Page, UserProfile
from django.urls import reverse

def index(request):
    context_dict = {}
    category_list = Category.objects.order_by('likes')[:5]
    context_dict['pages'] = None
    return render(request, 'wheninrome/index.html', context=context_dict)

def about(request):
    context_dict = {}
    print(request.method)
    print(request.user)
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'wheninrome/about.html', context = context_dict)
    return response

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
    return render(request, 'wheninrome/index.html', context=context_dict)

@login_required
def add_category(request):
    pass

@login_required
def add_page(request, category_name_slug):
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

    return render(
        request,
        'WhenInRome/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
        }
    )

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('WhenInRome:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'WhenInRome/login.html')
    
@login_required
def restricted(request):
    return render(request, 'wheninrome/index.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('WhenInRome:index'))

@login_required
def profile(request, username):
    selected_user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=selected_user)

    is_following = False
    if request.user in user_profile.followers.all():
        is_following = True

    context_dict = {
        'selected_user': selected_user,
        'user_profile': user_profile,
        'is_following': is_following,
        'follower_count': user_profile.followers.count(),
    }

    return render(request, 'WhenInRome/profile.html', context=context_dict)

@login_required
def follow_user(request, username):
    if request.method == 'POST':
        selected_user = get_object_or_404(User, username=username)

        if request.user == selected_user:
            return redirect(reverse('WhenInRome:profile', kwargs={'username': username}))

        user_profile, created = UserProfile.objects.get_or_create(user=selected_user)

        if request.user in user_profile.followers.all():
            user_profile.followers.remove(request.user)
        else:
            user_profile.followers.add(request.user)

        return redirect(reverse('WhenInRome:profile', kwargs={'username': username}))

    return redirect(reverse('WhenInRome:index'))


@login_required
def list_profiles(request):
    profiles = UserProfile.objects.all()
    return render(
        request,
        'WhenInRome/list_profiles.html',
        {'userprofile_list': profiles}
    )

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

