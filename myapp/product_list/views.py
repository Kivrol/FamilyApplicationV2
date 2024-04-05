from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms
from main.models import UserProfile
from . import models


# Create your views here.
class ProductList(View):
    def get(self, request, *args, **kwargs):
        form = forms.AddProduct()
        products = models.ProductListComponent.objects.filter(family=UserProfile.objects.get(user=request.user).family)
        return render(request, 'main/product_list.html', {'form': form, 'products': products})

    def post(self, request, *args, **kwargs):
        form = forms.AddProduct(request.POST)
        if form.is_valid():
            new_prod = form.save(commit=False)
            new_prod.family = UserProfile.objects.get(user=request.user).family
            new_prod.save()
        return redirect('product_list')


class DeleteProduct(View):
    def get(self, request, *args, **kwargs):
        models.ProductListComponent.objects.filter(id=kwargs['id']).delete()
        return redirect('product_list')