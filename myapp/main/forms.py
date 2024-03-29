from django import forms
from django.core.validators import FileExtensionValidator
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Family, ProductListComponent, WishListComponent, CloudFile


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

    class Meta:
        model = UserProfile
        fields = ['patronimic', 'profileAvatar']


class MyAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': "This account is inactive.",
    }


class WishListForm(forms.ModelForm):
    class Meta:
        model = WishListComponent
        exclude = ['date', 'user_profile']

    # TODO подумать, надо ли оно вообще
    def clean_custom_reason(self):
        if self.cleaned_data['reason'] == 'др' and self.cleaned_data['custom_reason'] is None:
            return "Другое"


class UploadVideoFile(forms.ModelForm):
    class Meta:
        model = CloudFile
        fields = ['video_file']


