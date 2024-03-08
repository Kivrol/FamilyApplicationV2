from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='calendar'),
    path('profile', views.profileView, name='profile'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name = 'login'),
    path('logout/', views.logout, name='logout'),
    # path('signin/', views.login, name='signin'),
    # path('registration/', views.registration, name='registration'),
    # path('registration/backtoregexist', views.regExist, name='regexist'),
    # path('signin/backtologexist', views.logExist, name='logexist')
]
