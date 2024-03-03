from django import forms
from .models import AuthUserData


class RegisterUserForm(forms.Form):
    userName = forms.CharField(max_length=50, min_length=5, required=True,
                               error_messages={
                                   'min_length': 'Длина должна быть больше 5 символов',
                                   'max_length': 'Длина должна быть мельше 50 символов'
                               })
    password = forms.CharField(max_length=50, min_length=8, required=True,
                               error_messages={
                                   'min_length': 'Длина должна быть больше 8 символов',
                                   'max_length': 'Длина должна быть мельше 50 символов'
                               })
    name = forms.CharField(max_length=50, required=True,
                               error_messages={
                                   'max_length': 'Длина должна быть мельше 50 символов'
                               })


# class RegisterUserForm(forms.ModelForm):
#     class Meta:
#         model = AuthUserData
#         fields = ['userName', 'password', 'name']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }
