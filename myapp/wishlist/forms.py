from django import forms

from .models import WishListComponent


class WishListForm(forms.ModelForm):
    class Meta:
        model = WishListComponent
        exclude = ['date', 'user_profile']

    # TODO подумать, надо ли оно вообще
    def clean_custom_reason(self):
        if self.cleaned_data['reason'] == 'др' and self.cleaned_data['custom_reason'] is None:
            return "Другое"
