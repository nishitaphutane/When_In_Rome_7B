from django.urls import path
from WhenInRome import views

app_name ='WhenInRome'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    #added this part
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profiles/', views.list_profiles, name='list_profiles'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('upvote/<int:recommendation_id>/', views.recommendation_upvotes, name='recommendation_upvotes'),
    path('add_review/<int:recommendation_id>/', views.add_review, name='add_review'),
]
