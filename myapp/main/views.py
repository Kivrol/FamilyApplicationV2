import json

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View

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
        return render(request, 'main/family.html', {'family': family, 'is_creator': is_creator})


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


# Доработать редактирование профиля, нужно сделать проверку на пустые поля, и если они пустые, то не заменять поля в БД
class EditProfile(View):
    def get(self, request, *args, **kwargs):
        userForm = EditUserForm(instance=request.user)

        up = UserProfile.objects.get(user=request.user)
        profileForm = EditProfileForm(instance=UserProfile.objects.get(user=request.user))

        changePass = PasswordChangeForm(request.user)

        return render(request, 'main/editprofile.html', {'userForm': userForm, 'profileForm': profileForm, "changePass": changePass})

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
        form.fields['family'].queryset = Family.objects
        return render(request, 'main/join_family_request.html', {'form': form, 'req_list': req_list})

    def post(self, request, *args, **kwargs):
        form = AddFamilyRequest(request.POST)
        form.fields['family'].queryset = Family.objects
        if form.is_valid():
            for f in JoinFamilyRequest.objects.all():
                if f.family == form.cleaned_data['family'] and f.user == request.user and f.accepted == False:
                    messages.error(request, 'Запрос в эту группу уже отправлен')
                    return redirect('join_family')
            JoinFamilyRequest(user=request.user, family=form.cleaned_data['family']).save()
            return redirect('family')
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


# class Calendar(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'main/calendar.html', {'items': CalendarItem.objects.all()})
#
#
# class CalendarApi(View):
#     def get(self, request, *args, **kwargs):
#         print(kwargs['month'], kwargs['year'])
#         month = int(kwargs['month'])
#         year = int(kwargs['year'])
#         prev_month = month - 1
#         prev_year = year
#         if prev_month == 0:
#             prev_month = 12
#             prev_year = year - 1
#         next_month = month + 1
#         if next_month > 12:
#             next_month = 1
#         items = CalendarItem.objects.filter(
#             Q(start__year=year) & Q(start__month=month) | (
#                     Q(start__year=prev_year) & Q(start__month=prev_month) & Q(end__month=month))
#         )
#         base = calendar.monthcalendar(year, month)
#         print(base)
#         new_base = []
#         for i in base:
#             for j in i:
#                 new_base.append(j)
#         future_json = []
#         for day in new_base:
#             future_json.append(dict(
#                 {'active': day != 0 and day >= datetime.datetime.now().day and month == datetime.datetime.now().month,
#                  'day': day, 'dow': calendar.weekday(year, month, day) if day != 0 else 0,
#                  'items': list()}))
#         for item in items:
#             print("ITEM ", item)
#             print("START DAY ", item.start.day)
#             if item.start.month == month and item.end.month == month:
#                 for day in range(item.start.day, item.end.day + 1):
#                     future_json[day - 1 + calendar.weekday(year, month, 1)]['items'].append(item.title)
#             elif item.end.month == month:
#                 for day in range(1, item.end.day + 1):
#                     future_json[day - 1 + calendar.weekday(year, month, 1)]['items'].append(item.title)
#             elif item.end.month == next_month:
#                 for day in range(item.start.day, calendar.monthrange(year, month)[1] + 1):
#                     future_json[day - 1 + calendar.weekday(year, month, 1)]['items'].append(item.title)
#             print("END DAY ", item.end.day)
#         print(json.dumps(future_json, indent=4, sort_keys=True))
#         return JsonResponse(future_json, safe=False)
#
#
# class AddCalendarItem(View):
#     def get(self, request):
#         form = AddCalendarItemForm()
#         return render(request, 'main/add_calendar_item.html', {'form': form})
#
#     def post(self, request):
#         form = AddCalendarItemForm(request.POST)
#         if form.is_valid():
#             item = form.save(commit=False)
#             item.creator = UserProfile.objects.get(user=request.user)
#             item.group = item.creator.family
#             item.save()
#             return redirect('calendar')
#         else:
#             return render(request, 'main/add_calendar_item.html', {'form': form})
#
#
# class CalendarDetailApi(View):
#     def get(self, request, *args, **kwargs):
#         item = CalendarItem.objects.get(id=kwargs['id'])
#         data = dict()
#         data['id'] = item.id
#         data['title'] = item.title
#         data['group'] = item.group.id
#         data['creator'] = item.creator.id
#         data['start'] = item.start
#         data['end'] = item.end
#         data['description'] = item.description
#         data['notification'] = item.notification
#         data['icon'] = item.icon
#         return JsonResponse(data, safe=False)
#
#
# class DeleteCalendarItem(View):
#     def get(self, request, *args, **kwargs):
#         CalendarItem.objects.get(id=kwargs['id']).delete()
#         return redirect('calendar')
