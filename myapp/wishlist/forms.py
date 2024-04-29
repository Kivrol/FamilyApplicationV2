from django import forms

from .models import WishListComponent


class WishListForm(forms.ModelForm):
    class Meta:
        model = WishListComponent
        exclude = ['date', 'user_profile']


