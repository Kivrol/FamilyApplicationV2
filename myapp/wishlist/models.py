from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from main.models import UserProfile


class WishListComponent(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Наименование')
    picture = models.ImageField(
        upload_to=f'wishImg/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico', 'jpeg', 'webp'])],
        verbose_name='Картинка',
        name='wish_picture'
    )
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    date = models.DateField(verbose_name='Дата добавления', default=timezone.now)
    active = models.BooleanField(default=True)
    reason = models.CharField(max_length=100, verbose_name='Причина', null=True, choices=(('Новый год', 'Новый год'),
                                                                                          ('Свадьба', 'Свадьба'),
                                                                                          ('День рождения', 'День Рождения'),
                                                                                          ('8 марта', '8 Марта'),
                                                                                          ('23 февраля', '23 Февраля'),
                                                                                          ('Другое', 'Другое')),
                              default="Другое")
    custom_reason = models.CharField(max_length=100, verbose_name='Примечание', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        if self.active:
            return f" {self.user_profile.user.username} хочет {self.name}"
        else:
            return f" {self.user_profile.user.username} скрыл, что хочет {self.name}"

    class Meta:
        verbose_name = 'Желание'
        verbose_name_plural = 'Желания'