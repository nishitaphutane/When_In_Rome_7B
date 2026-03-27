import datetime
from django.db import models
from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from WhenInRome.models import City, Recommendation, UserProfile,Review,Upvote
from WhenInRome.forms import UserForm, UserProfileForm, RecommendationForm, CityForm, ReviewForm
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def upload_recommendation(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST, request.FILES)
        if form.is_valid():
            category_value = request.POST.get('category', '').strip()
            city = City.objects.filter(slug=category_value).first()

            if not city:
                city = City.objects.filter(name__iexact=category_value).first()

            if not city:
                return JsonResponse(
                    {"error": f"Category '{category_value}' not found."},
                    status=400
                )

            recommendation = form.save(commit=False)
            recommendation.city = city
            recommendation.user = request.user
            recommendation.save()

            return JsonResponse({"success": True})
        else:
            return JsonResponse({"error": "Invalid form data.", "fields": form.errors}, status=400)

    cities = City.objects.all()
    return render(request, 'WhenInRome/upload_recommendation.html', {'cities': cities})
def index(request):
    city_list = City.objects.annotate(total_upvotes=Count('recommendation__upvote')).order_by('-total_upvotes')[:5]
    context_dict = {'categories': city_list}
    return render(request, 'WhenInRome/index.html', context=context_dict)

def about(request):
    context_dict = {}
    print(request.method)
    print(request.user)
    response = render(request, 'WhenInRome/about.html', context = context_dict)
    return response

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        city = City.objects.get(slug=category_name_slug)
        pages = Recommendation.objects.filter(city=city)
        context_dict['pages'] = pages
        context_dict['city'] = city
    except City.DoesNotExist:
        context_dict['city'] = None
    return render(request, 'WhenInRome/category.html', context_dict)

@login_required
def add_category(request):
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        return redirect(reverse('WhenInRome:index'))
    else:
        print(form.errors)
    return render(request, 'WhenInRome/category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = City.objects.get(slug=category_name_slug)
    except City.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('WhenInRome:index'))
    
    form = RecommendationForm()

    if request.method == 'POST':
        form = RecommendationForm(request.POST, request.FILES)
    
    if form.is_valid():
        if category:
            recommendation = form.save(commit=False)
            recommendation.city = category
            recommendation.user = request.user
            recommendation.save()

            return redirect(reverse('WhenInRome:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    else:
        form = RecommendationForm()
    return render(request, 'WhenInRome/add_page.html', {'form': form, 'category': category}) 

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

def view_reviews(request):
    reviews = Review.objects.filter(recommendation=recommendation).order_by('-created_at')

    return render(request, 'your_template.html', {
        'recommendation': recommendation,
        'reviews': reviews
    })

@login_required
def add_review(request, recommendation_id):
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)

    # GET → show page
    if request.method == 'GET':
        form = ReviewForm()
        return render(request, 'WhenInRome/add_review.html', {
            'form': form,
            'recommendation': recommendation
        })

    # POST → return JSON
    if request.method == 'POST':

        if Review.objects.filter(user=request.user, recommendation=recommendation).exists():
            return JsonResponse({"error": "You have already reviewed this recommendation."}, status=400)

        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.recommendation = recommendation
            review.user = request.user
            review.save()

            return JsonResponse({
                "success": True,
                "review": {
                    "username": request.user.username,
                    "rating": review.rating,
                    "comment": review.comment,
                }
            }, status=201)

        return JsonResponse({"error": "Invalid data.", "fields": form.errors}, status=400)

@login_required
def upload_picture(request):
    if request.method == 'POST':
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid():
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
            profile_form.save()
            messages.success(request, 'Profile picture updated successfully.')
        else:
            messages.error(request, 'Failed to update profile picture.')

    return redirect(reverse('WhenInRome:profile', kwargs={'username': request.user.username}))

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        profile.pronouns = request.POST.get('pronouns', '').strip()
        profile.city = request.POST.get('city', '').strip()
        profile.country = request.POST.get('country', '').strip()
        if 'location_flag' in request.FILES:
            profile.location_flag = request.FILES['location_flag']
        profile.save()
    return redirect('WhenInRome:profile', username=request.user.username)


@login_required
def update_visited(request):
    if request.method == 'POST':
        cities = [c.strip() for c in request.POST.getlist('visited_city') if c.strip()]
        flags = request.FILES.getlist('visited_flag')

        request.user.visited_cities.all().delete()

        for i, city_name in enumerate(cities):
            city = request.user.visited_cities.create(city_name=city_name)
            if i < len(flags) and flags[i]:
                city.flag_image = flags[i]
                city.save()

    return redirect('WhenInRome:profile', username=request.user.username)

