from django.shortcuts import render, redirect
from django.views.generic import View
from main.models import UserProfile
from .forms import WishListForm
from .models import WishListComponent


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