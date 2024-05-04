import datetime

from django import forms
from django.core.validators import FileExtensionValidator
from django.utils import timezone

from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Family
from django.contrib.admin import widgets


class AddFamily(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name', 'familyAvatar']


class AddFamilyRequest(forms.Form):
    family = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))


class UpdateFamily(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name', 'familyAvatar']


class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length=191, required=False,
                               error_messages={
                                   'max_length': 'Длина должна быть меньше 191 символов',
                                   'unique': 'Это имя пользователя уже занято'
                               })
    first_name = forms.CharField(max_length=191, required=False,
                                 error_messages={
                                     'max_length': 'Длина должна быть меньше 191 символов'
                                 })
    last_name = forms.CharField(max_length=191, required=False,
                                error_messages={
                                    'max_length': 'Длина должна быть меньше 191 символов'
                                })

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class EditProfileForm(forms.ModelForm):
    patronimic = forms.CharField(max_length=191, required=False,
                                 error_messages={
                                     'max_length': 'Длина должна быть меньше 191 символов'
                                 })
    profileAvatar = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico'])],
    )

    birthDate = forms.DateField(required=False)

    class Meta:
        model = UserProfile
        fields = ['patronimic', 'profileAvatar', 'birthDate', 'phoneNumber']


class MyAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': "This account is inactive.",
    }
