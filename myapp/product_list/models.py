from django.db import models
from django.utils import timezone
from main.models import Family


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
