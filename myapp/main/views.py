from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Family, UserProfile, JoinFamilyRequest, ProductListComponent
from .forms import RegisterForm, LoginForm, AddFamily, AddFamilyRequest, AddProduct, EditProfileDefault


@login_required
def index(request):
    return render(request, 'main/index.html')


@login_required
def profileView(request):
    template_name = 'main/profile.html'
    return render(request, template_name)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('profile'))
        else:
            return redirect('login')


class FamilyView(View):
    def get(self, request):
        family = UserProfile.objects.get(user=request.user).family
        return render(request, 'main/family.html', {'family': family})


class CreateFamily(View):
    def get(self, request):
        form = AddFamily()
        return render(request, 'main/addfamily.html', {'form': form})

    def post(self, request):
        form = AddFamily(request.POST, request.FILES)
        if form.is_valid():
            family = Family(name=form.cleaned_data['name'], familyAvatar=form.cleaned_data['familyAvatar'])
            family.creator = request.user
            prof = UserProfile.objects.get(user=request.user)
            prof.family = family
            family.save()
            prof.save()
            form.save(commit=False)
            return redirect('profile')
        else:
            print(form.errors)
            return redirect('add_family')


class DeleteFamily(View):
    def get(self, request, *args, **kwargs):
        Family.objects.get(id=kwargs['id']).delete()
        return redirect('profile')


class RegistrationView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'main/registration.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
            return redirect('registration')


def view_logout(request):
    logout(request)
    return redirect('profile')


class EditProfile(View):
    def get(self, request, *args, **kwargs):
        form = EditProfileDefault()
        return render(request, 'main/editprofile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EditProfileDefault(request.POST, request.FILES)
        if form.is_valid():
            # userName = form.cleaned_data["editUserName"]
            # name = form.cleaned_data["editName"]
            # surname = form.cleaned_data["editSurname"]
            # patronimic = form.cleaned_data["editPatronymic"]
            # avatar = form.cleaned_data["editAvatar"]
            return redirect('editprofile')
        else:
            return redirect('profile')


class JoinFamilyRequestView(View):
    def get(self, request, *args, **kwargs):
        form = AddFamilyRequest()
        form.user = request.user
        form.fields['family'].queryset = Family.objects
        return render(request, 'main/join_family_request.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddFamilyRequest(request.POST)
        form.fields['family'].queryset = Family.objects
        if form.is_valid():
            JoinFamilyRequest(user=request.user, family=form.cleaned_data['family']).save()
            return redirect('family')
        return redirect('join_family')


class ProcessRequest(View):
    def get(self, request, *args, **kwargs):
        try:
            requests = JoinFamilyRequest.objects.filter(family=Family.objects.filter(creator=request.user)[0])
        except:
            requests = None
        return render(request, 'main/accept_family_request.html', {'requests': requests})


class AcceptRequest(View):
    def get(self, request, *args, **kwargs):
        try:
            req = JoinFamilyRequest.objects.filter(id=kwargs['id'])[0]
        except IndexError:
            return redirect('process_request')
        profile = UserProfile.objects.get(user=req.user)
        profile.family = req.family
        profile.save()
        return redirect('family')


class DeclineRequest(View):
    def get(self, request, *args, **kwargs):
        try:
            req = JoinFamilyRequest.objects.filter(id=kwargs['id'])[0]
        except IndexError:
            return redirect('process_request')
        req.delete()
        return redirect('process_request')


class ProductList(View):
    def get(self, request, *args, **kwargs):
        form = AddProduct()
        products = ProductListComponent.objects.filter(family=UserProfile.objects.get(user=request.user).family)
        return render(request, 'main/product_list.html', {'form': form, 'products': products})

    def post(self, request, *args, **kwargs):
        form = AddProduct(request.POST)
        if form.is_valid():
            new_prod = form.save(commit=False)
            new_prod.family = UserProfile.objects.get(user=request.user).family
            new_prod.save()
        return redirect('product_list')

class DeleteProduct(View):
    def get(self, request, *args, **kwargs):
        ProductListComponent.objects.filter(id=kwargs['id']).delete()
        return redirect('product_list')
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
