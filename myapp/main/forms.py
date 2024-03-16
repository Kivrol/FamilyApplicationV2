from django import forms
from django.core.validators import FileExtensionValidator

from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from .models import Family, ProductListComponent


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        for user in User.objects.all():
            if user.email == self.cleaned_data['email']:
                raise ValidationError("Email must be unique!")


class AddFamily(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name', 'familyAvatar']


class AddFamilyRequest(forms.Form):
    family = forms.ModelChoiceField(queryset=None)


class AddProduct(forms.ModelForm):
    class Meta:
        model = ProductListComponent
        fields = ['name', 'unit', 'amount']


class EditUserForm(forms.Form):
    username = forms.CharField(max_length=191, required=False,
                               error_messages={
                                   'max_length': 'Длина должна быть меньше 191 символов'
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


class EditProfileForm(forms.Form):
    patronimic = forms.CharField(max_length=191, required=False,
                                 error_messages={
                                     'max_length': 'Длина должна быть меньше 191 символов'
                                 })
    profileAvatar = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico'])],
    )

    class Meta:
        model = UserProfile
        fields = ['patronimic', 'profileAvatar']

# class RegisterUserForm(forms.Form):
#     userName = forms.CharField(max_length=50, min_length=5, required=True,
#                                error_messages={
#                                    'min_length': 'Длина должна быть больше 5 символов',
#                                    'max_length': 'Длина должна быть мельше 50 символов'
#                                })
#     password = forms.CharField(max_length=50, min_length=8, required=True,
#                                error_messages={
#                                    'min_length': 'Длина должна быть больше 8 символов',
#                                    'max_length': 'Длина должна быть мельше 50 символов'
#                                })
#     name = forms.CharField(max_length=50, required=True,
#                                error_messages={
#                                    'max_length': 'Длина должна быть мельше 50 символов'
#                                })
#
#
# class AuthUserForm(forms.Form):
#     userName = forms.CharField(max_length=50, min_length=5, required=True,
#                                error_messages={
#                                    'min_length': 'Длина должна быть больше 5 символов',
#                                    'max_length': 'Длина должна быть мельше 50 символов'
#                                })
#     password = forms.CharField(max_length=50, min_length=8, required=True,
#                                error_messages={
#                                    'min_length': 'Длина должна быть больше 8 символов',
#                                    'max_length': 'Длина должна быть мельше 50 символов'
#                                })


# class RegisterUserForm(forms.ModelForm):
#     class Meta:
#         model = AuthUserData
#         fields = ['userName', 'password', 'name']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }
