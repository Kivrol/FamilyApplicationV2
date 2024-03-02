from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='calendar'),
    path('profile', views.profileView, name='profile'),
    path('login', views.login, name='login'),
    path('registration', views.registration, name='registration'),
]