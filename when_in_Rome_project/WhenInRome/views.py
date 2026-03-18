import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from WhenInRome.forms import UserForm, UserProfile

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
        profile_form = UserProfileForm(request.POST)

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

    return render(request, 'wheninrome/index.html', context = {'user_form' : user_form,
                                                               'profile_form' : profile_form,
                                                               'registered' : registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('wheninrome/index.html'))
            else:
                return HttpResponse('Your When In Rome account is disabled.')
        else:
            print('Invalid login details: {username}, {password}')
            return HttpResponse('Invalid login details supplied.')
    else:
        return render(request, 'wheninrome/index.html')
    
@login_required
def restricted(request):
    return render(request, 'wheninrome/index.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reversed('wheninrome/index.html'))

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

