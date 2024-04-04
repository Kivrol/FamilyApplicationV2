import json

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic import View, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from .models import Family, UserProfile, JoinFamilyRequest, ProductListComponent, WishListComponent, CloudFile, \
    CalendarItem
from .forms import RegisterForm, AddFamily, AddFamilyRequest, AddProduct, EditUserForm, EditProfileForm, WishListForm, \
    UploadVideoFile, UploadPhotoFile, UploadDocFile, UploadArchiveFile, AddCalendarItemForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import calendar


@login_required
def index(request):
    return render(request, 'main/index.html')


@login_required
def profileView(request):
    template_name = 'main/profile.html'
    return render(request, template_name)


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('profile')

        return render(request, 'registration/login.html', {'form': form})


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
            return render(request, 'main/registration.html', {'form': form})


def view_logout(request):
    logout(request)
    return redirect('profile')


# Доработать редактирование профиля, нужно сделать проверку на пустые поля, и если они пустые, то не заменять поля в БД
class EditProfile(View):
    def get(self, request, *args, **kwargs):
        userForm = EditUserForm(instance=request.user)

        up = UserProfile.objects.get(user=request.user)
        profileForm = EditProfileForm(instance=UserProfile.objects.get(user=request.user))

        return render(request, 'main/editprofile.html', {'userForm': userForm, 'profileForm': profileForm})

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


class WishListMainPage(View):
    def get(self, request, *args, **kwargs):
        ups = UserProfile.objects.filter(family=UserProfile.objects.get(user=request.user).family)
        users = [up.user for up in ups]
        if request.user in users:
            users.insert(0, users.pop(users.index(request.user)))
        return render(request, 'main/wishlist.html', {'users': users})


class WishListUser(View):
    def get(self, request, *args, **kwargs):
        user = UserProfile.objects.get(user=kwargs['user'])
        showform = (request.user == user.user)
        if showform:
            wishes = WishListComponent.objects.filter(user_profile=user)
        else:
            wishes = WishListComponent.objects.filter(user_profile=user, active=True)
        form = WishListForm()

        return render(request, 'main/wishlist_user.html',
                      {'wishes': wishes, 'user_': user, 'form': form, 'showform': showform})

    def post(self, request, *args, **kwargs):
        form = WishListForm(request.POST)
        user = UserProfile.objects.get(user=request.user)
        wishes = WishListComponent.objects.filter(user_profile=user)
        showform = True
        if form.is_valid():
            print(form.cleaned_data['custom_reason'])
            wish = form.save(commit=False)
            print(wish.custom_reason)
            wish.user_profile = UserProfile.objects.get(user=request.user)
            wish.save()
            return redirect('wishlistuser', user=request.user.id)
        else:
            return render(request, 'main/wishlist_user.html',
                          {'wishes': wishes, 'user_': user, 'form': form, 'showform': showform})


class WishChangeActive(View):
    def get(self, request, *args, **kwargs):
        wish = WishListComponent.objects.get(id=kwargs['id'])
        wish.active = not wish.active
        wish.save()
        return redirect('wishlistuser', user=request.user.id)


class WishDelete(View):
    def get(self, request, *args, **kwargs):
        WishListComponent.objects.get(id=kwargs['id']).delete()
        return redirect('wishlistuser', user=request.user.id)


class WishEdit(View):
    def get(self, request, *args, **kwargs):
        wish = WishListComponent.objects.get(id=kwargs['pk'])
        form = WishListForm(instance=wish)
        return render(request, 'main/wishlist_user.html', {'form': form, 'showform': True, 'wish': wish})

    def post(self, request, *args, **kwargs):
        wish = WishListComponent.objects.get(id=request.POST['wid'])
        form = WishListForm(request.POST, instance=wish)
        if form.is_valid():
            form.save()
        return redirect('wishlistuser', user=request.user.id)


class Cloud(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/cloud.html')


class CloudVideo(View):
    def get(self, request, *args, **kwargs):
        files = CloudFile.objects.filter(category='video', family=UserProfile.objects.get(user=request.user).family)
        form = UploadVideoFile()
        return render(request, 'main/cloud_video.html', {'files': files, 'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadVideoFile(request.POST, request.FILES)
        files = CloudFile.objects.filter(category='video', family=UserProfile.objects.get(user=request.user).family)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.family = UserProfile.objects.get(user=request.user).family
            new_file.owner = request.user
            new_file.category = 'video'
            new_file.save()
        else:
            return render(request, 'main/cloud_video.html', {'files': files, 'form': form})
        return redirect('cloud_video')


class DeleteVideoFile(View):
    def get(self, request, *args, **kwargs):
        CloudFile.objects.get(id=kwargs['id']).delete()
        print(request)
        return redirect('cloud_video')

    def post(self, request, *args, **kwargs):
        todel = json.loads(request.POST['data'])
        for i, v in todel.items():
            if v:
                CloudFile.objects.get(id=i).delete()
        return redirect('cloud_video')


class CloudPhoto(View):
    def get(self, request, *args, **kwargs):
        files = CloudFile.objects.filter(category='photo', family=UserProfile.objects.get(user=request.user).family)
        form = UploadPhotoFile()
        return render(request, 'main/cloud_photo.html', {'files': files, 'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadPhotoFile(request.POST, request.FILES)
        files = CloudFile.objects.filter(category='photo', family=UserProfile.objects.get(user=request.user).family)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.family = UserProfile.objects.get(user=request.user).family
            new_file.owner = request.user
            new_file.category = 'photo'
            new_file.save()
        else:
            return render(request, 'main/cloud_photo.html', {'files': files, 'form': form})
        return redirect('cloud_photo')


class DeletePhotoFile(View):
    def get(self, request, *args, **kwargs):
        CloudFile.objects.get(id=kwargs['id']).delete()
        print(request)
        return redirect('cloud_photo')

    def post(self, request, *args, **kwargs):
        todel = json.loads(request.POST['data'])
        for i, v in todel.items():
            if v:
                CloudFile.objects.get(id=i).delete()
        return redirect('cloud_photo')


class CloudDoc(View):
    def get(self, request, *args, **kwargs):
        files = CloudFile.objects.filter(category='doc', family=UserProfile.objects.get(user=request.user).family)
        form = UploadDocFile()
        return render(request, 'main/cloud_doc.html', {'files': files, 'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadDocFile(request.POST, request.FILES)
        files = CloudFile.objects.filter(category='doc', family=UserProfile.objects.get(user=request.user).family)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.family = UserProfile.objects.get(user=request.user).family
            new_file.owner = request.user
            new_file.category = 'doc'
            new_file.save()
        else:
            return render(request, 'main/cloud_doc.html', {'files': files, 'form': form})
        return redirect('cloud_doc')


class DeleteDocFile(View):
    def get(self, request, *args, **kwargs):
        CloudFile.objects.get(id=kwargs['id']).delete()
        print(request)
        return redirect('cloud_doc')

    def post(self, request, *args, **kwargs):
        todel = json.loads(request.POST['data'])
        for i, v in todel.items():
            if v:
                CloudFile.objects.get(id=i).delete()
        return redirect('cloud_doc')


class CloudArchive(View):
    def get(self, request, *args, **kwargs):
        files = CloudFile.objects.filter(category='archive', family=UserProfile.objects.get(user=request.user).family)
        form = UploadArchiveFile()
        return render(request, 'main/cloud_archive.html', {'files': files, 'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadArchiveFile(request.POST, request.FILES)
        files = CloudFile.objects.filter(category='archive', family=UserProfile.objects.get(user=request.user).family)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.family = UserProfile.objects.get(user=request.user).family
            new_file.owner = request.user
            new_file.category = 'archive'
            new_file.save()
        else:
            return render(request, 'main/cloud_archive.html', {'files': files, 'form': form})
        return redirect('cloud_archive')


class DeleteArchiveFile(View):
    def get(self, request, *args, **kwargs):
        CloudFile.objects.get(id=kwargs['id']).delete()
        print(request)
        return redirect('cloud_archive')

    def post(self, request, *args, **kwargs):
        todel = json.loads(request.POST['data'])
        for i, v in todel.items():
            if v:
                CloudFile.objects.get(id=i).delete()
        return redirect('cloud_archive')


class Calendar(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/calendar.html', {'items': CalendarItem.objects.all()})


class CalendarApi(View):
    def get(self, request, *args, **kwargs):
        print(kwargs['month'], kwargs['year'])
        month = int(kwargs['month'])
        year = int(kwargs['year'])
        items = CalendarItem.objects.filter(
            Q(start__year=year) & Q(start__month=month)
        )
        base = calendar.monthcalendar(year, month)
        print(base)
        new_base = []
        for i in base:
            for j in i:
                new_base.append(j)
        future_json = []
        for day in new_base:
            future_json.append(dict(
                {'active': day != 0, 'day': day, 'dow': calendar.weekday(year, month, day) if day != 0 else 0,
                 'items': list()}))
        for item in items:
            print("ITEM ", item)
            print("START DAY ", item.start.day)
            for day in range(item.start.day, item.end.day + 1):
                future_json[day - 1 + calendar.weekday(year, month, 1)]['items'].append(item.title)
            print("END DAY ", item.end.day)
            # future_json[item.start.day+calendar.weekday(year, month, 1)-1]['items'].append(item.title)
        print(json.dumps(future_json, indent=4, sort_keys=True))
        return JsonResponse(future_json, safe=False)


class AddCalendarItem(View):
    def get(self, request):
        form = AddCalendarItemForm()
        return render(request, 'main/add_calendar_item.html', {'form': form})

    def post(self, request):
        form = AddCalendarItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.creator = UserProfile.objects.get(user=request.user)
            item.group = item.creator.family
            item.save()
            return redirect('calendar')
        else:
            return render(request, 'main/add_calendar_item.html', {'form': form})
