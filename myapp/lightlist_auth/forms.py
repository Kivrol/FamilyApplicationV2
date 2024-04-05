from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    username = forms.CharField(error_messages={'unique': 'Пользователь с таким именем уже существует'})
    password2 = forms.CharField(error_messages={'too_short': 'Пароль слишком короткий',
                                                'too_similar': 'Пароль слишком похож на юзернейм',
                                                'password_too_common': 'Пароль слишком распространённый',
                                                'password_entirely_numeric': 'Пароль состоит целиком из цифр'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        for user in User.objects.all():
            if user.email == self.cleaned_data['email']:
                raise ValidationError("Электронная почта должна быть уникальной")