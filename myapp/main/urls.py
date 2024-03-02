from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='calendar'),
    path('profile', views.profileView, name='profile'),
]