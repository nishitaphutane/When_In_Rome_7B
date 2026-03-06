from django.urls import path
from WhenInRome import views

app_name ='When In Rome'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about')
]
