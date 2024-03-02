from django.db import models
from django.core.validators import FileExtensionValidator


class AuthUserData(models.Model):
    # модель пользователя (БД)
    userName = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    phoneNumber = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    joinDate = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50, null=True, blank=True)
    patronimic = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(
        upload_to=f'',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg, png, ico'])]
        )

    @property
    def isAuthenticated(self):
        # Возвращает True если пользователь аутентифицирован
        return True
