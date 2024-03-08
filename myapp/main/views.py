from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


# from .models import AuthUserData
# from .forms import RegisterUserForm, AuthUserForm


def index(request):
    return render(request, 'main/index.html')


@login_required
def profileView(request):
    template_name = 'main/profile.html'
    return render(request, template_name)


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'main/profile.html'
    success_url = reverse_lazy('login')
    # Здесь не работает email, не сохраняется в БД при регистрации


def logout(request):
    logout(request)
    redirect('profile')


# def login(request):
#     template_name = 'main/signin.html'
#     form = AuthUserForm()
#     if request.method == 'POST':
#         form = AuthUserForm(request.POST)
#         if form.is_valid():
#             userName = form.cleaned_data['userName']
#             password = form.cleaned_data['password']
#             if AuthUserData.objects.filter(userName=userName).exists():
#                 user = AuthUserData.objects.get(userName=userName)
#                 if password == user.password:
#                     return redirect('profile')
#                 else:
#                     return render(request, 'main/backtologexist.html')
#             else:
#                 return render(request, 'main/backtologexist.html')
#         else:
#             form = AuthUserForm()
#             return render(request, template_name, {'form': form})
#     return render(request, template_name, {'form': form})
#
#
# def logExist(request):
#     return render(request, 'main/backtologexist.html')
#
#
# def registration(request):
#     template_name = 'main/registration.html'
#     form = RegisterUserForm()
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             userName = form.cleaned_data['userName']
#             password = form.cleaned_data['password']
#             name = form.cleaned_data['name']
#             isNewUsername = AuthUserData.objects.filter(userName=userName).exists()
#             if not isNewUsername:
#                 AuthUserData.objects.create(userName=userName, password=password, name=name)
#                 return redirect('signin')
#             else:
#                 return render(request, 'main/backtoregexist.html')
#         else:
#             form = RegisterUserForm()
#             return render(request, template_name, {'form': form})
#
#     return render(request, template_name, {'form': form})
#
#
# def regExist(request):
#     return render(request, 'main/backtoregexist.html')
