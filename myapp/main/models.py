from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
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
        if self.accepted:
            return f"{self.user} принят в {self.family}"
        else:
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


class WishListComponent(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Наименование')
    picture = models.ImageField(
        upload_to=f'wishImg/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico'])],
        verbose_name='Картинка',
        name='wish_picture'
    )
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    date = models.DateField(verbose_name='Дата добавления', default=timezone.now)
    active = models.BooleanField(default=True)
    reason = models.CharField(max_length=100, verbose_name='Причина', null=True, choices=(('нг', 'Новый год'),
                                                                                          ('св', 'Свадьба'),
                                                                                          ('др', 'День Рождения'),
                                                                                          ('wd', '8 Марта'),
                                                                                          ('md', '23 Февраля'),
                                                                                          ('др', 'Другое')),
                              default="другое")
    custom_reason = models.CharField(max_length=100, verbose_name='Своя причина', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        if self.active:
            return f" {self.user_profile.user.username} хочет {self.name}"
        else:
            return f" {self.user_profile.user.username} скрыл, что хочет {self.name}"

    class Meta:
        verbose_name = 'Желание'
        verbose_name_plural = 'Желания'


class CloudFile(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    video_file = models.FileField(upload_to='files/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'mov', 'webm', 'avi'])])
    photo_file = models.FileField(upload_to='files/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico', 'jpeg', 'bmp'])])
    doc_file = models.FileField(upload_to='files/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'odt', 'rtf', 'txt', 'ppt', 'pptx', 'xls', 'xlsx'])])
    archive_file = models.FileField(upload_to='files/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['zip', 'rar', '7z', 'tar', 'gz'])])
    category = models.CharField(max_length=50, null=True, blank=True, choices=(('photo', 'Изображение'),
                                                                               ('doc', 'Документ'),
                                                                               ('archive', 'Архив'),
                                                                               ('video', 'Видео')))
    objects = models.Manager()

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        if self.video_file:
            return f'{self.video_file}'
        elif self.photo_file:
            return f'{self.photo_file.name}'
        elif self.doc_file:
            return f'{self.doc_file.name}'
        elif self.archive_file:
            return f'{self.archive_file.name}'


class CalendarItem(models.Model):
    group = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name='Группа')
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Создатель')
    title = models.CharField(max_length=100, verbose_name='Название')
    start = models.DateTimeField(default=timezone.now, verbose_name='Начало', validators=[MinValueValidator(timezone.now()-timezone.timedelta(hours=1))])
    end = models.DateTimeField(null=True, blank=True, verbose_name='Конец')
    notification = models.DateTimeField(null=True, blank=True, verbose_name='Дата уведомления')
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Событие календаря'
        verbose_name_plural = 'События календаря'


@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def saveUserProfile(sender, instance, **kwargs):
    instance.userprofile.save()
