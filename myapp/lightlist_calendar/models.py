from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from main.models import Family, UserProfile


class CalendarItem(models.Model):
    group = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name='Группа', )
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Создатель')
    title = models.CharField(max_length=100, verbose_name='Название')
    start = models.DateTimeField(default=timezone.now, verbose_name='Начало', validators=[MinValueValidator(timezone.now()-timezone.timedelta(hours=1))])
    end = models.DateTimeField(null=True, blank=True, verbose_name='Конец', validators=[MaxValueValidator(timezone.now() + timezone.timedelta(days=28))])
    notification = models.DateTimeField(null=True, blank=True, verbose_name='Дата уведомления')
    description = models.CharField(max_length=1000, verbose_name='Описание', null=True, blank=True)
    icon = models.CharField(max_length=100, verbose_name='Иконка', choices=(('work', 'Другое'),
                                                                            ('directions_walk', 'Прогулка'),
                                                                            ('apartment', 'Работа'),
                                                                            ('holiday_village', 'Дача'),
                                                                            ('celebration', 'День рождения'),
                                                                            ('park', 'Новый год'),
                                                                            ('favorite', 'День святого валентина'),
                                                                            ('woman', '8 Марта'),
                                                                            ('military_tech', '23 Февраля'),
                                                                            ('partner_exchange', 'Свадьба')), null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Событие календаря'
        verbose_name_plural = 'События календаря'
