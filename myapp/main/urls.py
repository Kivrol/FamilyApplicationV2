from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='calendar'),
    path('profile', views.profileView, name='profile'),
    path('signin/', views.login, name='signin'),
    path('registration/', views.registration, name='registration'),
    path('registration/backtoregexist', views.regExist, name='regexist'),
    path('signin/backtologexist', views.logExist, name='logexist')
]