import datetime
from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from WhenInRome.models import City, Recommendation, UserProfile,Review,Upvote
from WhenInRome.forms import UserForm, UserProfileForm, RecommendationForm, CityForm
from django.urls import reverse
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.models import User

def index(request):
    context_dict = {}
    city_list = City.objects.annotate(total_upvotes=Count('recommendation__upvote')).order_by('-total_upvotes')[:5]
    context_dict['pages'] = None
    return render(request, 'wheninrome/index.html', context=context_dict)

def about(request):
    context_dict = {}
    print(request.method)
    print(request.user)
    response = render(request, 'wheninrome/about.html', context = context_dict)
    return response

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = City.objects.get(slug=category_name_slug)
        pages = Recommendation.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except City.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'wheninrome/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        return redirect('/wheninrome/')
    else:
        print(form.errors)
    return render(request, 'wheninrome/category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = City.objects.get(slug=category_name_slug)
    except City.DoesNotExist:
        category = None

    if category is None:
        return redirect('/wheninrome/')
    
    form = RecommendationForm()

    if request.method == 'POST':
        form = RecommendationForm(request.POST)
    
    if form.is_valid():
        if category:
            recommendation = form.save(commit=False)
            recommendation.category = category
            recommendation.views = 0
            recommendation.save()

            return redirect(reverse('wheninrome:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

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

    is_following = request.user in user_profile.followers.all()
    follower_count = user_profile.followers.count()
    following_count = UserProfile.objects.filter(followers=selected_user).count()
    recommendations = Recommendation.objects.filter(user=selected_user)[:4]
    reviews = Review.objects.filter(user=selected_user)

    return render(request, 'WhenInRome/profile.html', {
        'selected_user': selected_user,
        'user_profile': user_profile,
        'is_following': is_following,
        'follower_count': follower_count,
        'following_count': following_count,
        'recommendations': recommendations,
        'reviews': reviews,
    })

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

@login_required
def recommendation_upvotes(request, recommendation_id):
    #Checks if request is POST
    if request.method == 'POST':
        recommendation = get_object_or_404(Recommendation, id=recommendation_id)
        user = request.user

        #Check if user already upvoted this recommendation
        existing_upvote = Upvote.objects.filter(user=user, recommendation=recommendation).first()

        #If upvoted remove it
        if existing_upvote:
            existing_upvote.delete()
            return JsonResponse({
                "Result": "Removed",
                "Upvotes": recommendation.upvote_count
            })
        else:
        #If not upvoted create new upvote
            Upvote.objects.create(user=user, recommendation=recommendation)
            return JsonResponse({
                "Result": "Added",
                "Upvotes": recommendation.upvote_count
            })
    #If not POST return error
    return JsonResponse({"Result": "Error"}, status=400)
