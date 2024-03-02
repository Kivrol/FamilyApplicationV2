from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')


def profileView(request):
    return render(request, 'main/profile.html')