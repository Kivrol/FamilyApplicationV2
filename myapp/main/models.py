import datetime
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, name='phoneNumber')
    birthDate = models.DateField(null=True, blank=True, name='birthDate')
    patronimic = models.CharField(max_length=50, null=True, blank=True, name='patronimic')
    avatar = models.ImageField(
        upload_to=f'UserProfileImg',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico'])],
        name='profileAvatar'
    )
    familyIdentifierName = models.CharField(max_length=100, null=True, blank=True)
    family = models.ForeignKey('Family', on_delete=models.SET_NULL, blank=True, null=True, name='family')
    objects = models.Manager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'UserProfile'


class Family(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Название', name='name')
    avatar = models.ImageField(
        upload_to=f'familyImg/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico'])],
        verbose_name='Аватар',
        name='familyAvatar'
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        if self.name is not None:
            return self.name
        return f'Семья №{self.id}'


class JoinFamilyRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.user} хочет вступить в {self.family}"

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'


class ProductListComponent(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Наименование')
    unit = models.CharField(max_length=2, choices=(('шт', 'шт'), ('кг', 'кг'), ('мл', 'мл')),
                            verbose_name='Мера измерения')
    amount = models.FloatField(verbose_name='Количество')
    date = models.DateField(verbose_name='Дата добавления', default=timezone.now)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name} - {self.amount} {self.unit} ({self.date})"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def saveUserProfile(sender, instance, **kwargs):
    instance.userprofile.save()

# class AuthUserData(models.Model):
#     # модель пользователя (БД)
#     userName = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
#     phoneNumber = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
#     birthDate = models.DateField(null=True, blank=True)
#     joinDate = models.DateField(auto_now_add=True)
#     name = models.CharField(max_length=50)
#     surname = models.CharField(max_length=50, null=True, blank=True)
#     patronimic = models.CharField(max_length=50, null=True, blank=True)
#     avatar = models.ImageField(
#         upload_to=f'',
#         null=True,
#         blank=True,
#         validators=[FileExtensionValidator(allowed_extensions=['jpg, png, ico'])]
#         )
#     familyIdentifierName = models.CharField(max_length=100, null=True, blank=True)
#
#     @property
#     def isAuthenticated(self):
#         # Возвращает True если пользователь аутентифицирован
#         return True
#
#     objects = models.Manager()
