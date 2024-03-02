from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'main/index.html')


@login_required
def profileView(request):
    return render(request, 'main/profile.html')


def login(request):
    return render(request, 'main/login.html')


def registration(request):
    return render(request, 'main/registration.html')
