import json

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View

from . import forms
from .models import Family, UserProfile, JoinFamilyRequest
from .forms import AddFamily, AddFamilyRequest, EditUserForm, EditProfileForm
from django.http import JsonResponse
import calendar
import datetime


@login_required
def index(request):
    return render(request, 'main/index.html')


@login_required
def profileView(request):
    template_name = 'main/profile.html'
    family = UserProfile.objects.get(user=request.user).family
    return render(request, template_name, {'family': family})


class FamilyView(View):
    def get(self, request):
        family = UserProfile.objects.get(user=request.user).family
        is_creator = False
        for f in Family.objects.all():
            if request.user == f.creator:
                is_creator = True
        form = forms.UpdateFamily(instance=family)
        return render(request, 'main/family.html', {'family': family, 'is_creator': is_creator, 'form': form})

    def post(self, request):
        form = forms.UpdateFamily(request.POST, request.FILES,
                                  instance=UserProfile.objects.get(user=request.user).family)
        if form.is_valid():
            form.save()
        return redirect('family')


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
        family = Family.objects.get(id=kwargs['id'])
        if family.creator == request.user:
            family.delete()
        return redirect('profile')


class ExitFromGroup(View):
    def get(self, request, *args, **kwargs):
        up = UserProfile.objects.get(user=request.user)
        family = Family.objects.get(id=kwargs['id'])
        if family.creator == request.user:
            if len(family.userprofile_set.all()) >= 2:
                family.creator = family.userprofile_set.all()[1].user
                family.save()
            else:
                family.delete()
        up.family = None
        up.save()
        return redirect('family')


class EditProfile(View):
    def get(self, request, *args, **kwargs):
        userForm = EditUserForm(instance=request.user)
        up = UserProfile.objects.get(user=request.user)
        profileForm = EditProfileForm(instance=UserProfile.objects.get(user=request.user))
        changePass = PasswordChangeForm(request.user)
        return render(request, 'main/editprofile.html',
                      {'userForm': userForm, 'profileForm': profileForm, "changePass": changePass})

    def post(self, request, *args, **kwargs):
        user = request.user
        userForm = EditUserForm(request.POST, instance=user)
        profileForm = EditProfileForm(request.POST, request.FILES, instance=UserProfile.objects.get(user=user))
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            return redirect('profile')

        else:
            return render(request, 'main/editprofile.html', {'userForm': userForm, 'profileForm': profileForm})


class ChangePassword(View):
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok'}, safe=False)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, safe=False)


class JoinFamilyRequestView(View):
    def get(self, request, *args, **kwargs):
        req_list = JoinFamilyRequest.objects.filter(user=request.user, accepted=False)
        form = AddFamilyRequest()
        form.user = request.user
        print(Family.objects.all())
        return render(request, 'main/join_family_request.html', {'form': form, 'req_list': req_list})

    def post(self, request, *args, **kwargs):
        form = AddFamilyRequest(request.POST)
        if form.is_valid():
            for f in JoinFamilyRequest.objects.all():
                if f.family.name == form.data['family'] and f.user == request.user and f.accepted == False:
                    messages.error(request, 'Запрос в эту группу уже отправлен')
                    return redirect('join_family')
            if form.data['family'] in [f.name for f in Family.objects.all()]:
                JoinFamilyRequest(user=request.user, family=Family.objects.get(name=form.data['family'])).save()
                messages.success(request, 'Запрос отправлен')
                return redirect('join_family')
            else:
                messages.error(request, 'Такой группы не существует')
                return redirect('join_family')
        print(form.errors)
        return redirect('join_family')


class ProcessRequest(View):
    def get(self, request, *args, **kwargs):
        try:
            requests = JoinFamilyRequest.objects.filter(family=Family.objects.filter(creator=request.user)[0],
                                                        accepted=False)
        except:
            requests = None
        return render(request, 'main/accept_family_request.html', {'requests': requests})


class AcceptRequest(View):
    def get(self, request, *args, **kwargs):
        try:
            req = JoinFamilyRequest.objects.filter(id=kwargs['id'])[0]
        except IndexError:
            return redirect('process_request')
        req.accepted = True
        req.save()
        for req in JoinFamilyRequest.objects.filter(user=request.user, accepted=False):
            req.delete()
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


class KickFromGroup(View):
    def get(self, request, *args, **kwargs):
        member = kwargs['member']
        profile = UserProfile.objects.get(id=member)
        profile.family = None
        profile.save()
        return redirect('family')
