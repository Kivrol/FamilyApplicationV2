# Generated by Django 5.0.3 on 2024-04-05 18:00

import datetime
import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_cloudfile_options_calendaritem'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendaritem',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='calendaritem',
            name='icon',
            field=models.CharField(blank=True, choices=[('birthday', 'День рождения'), ('wedding', 'Свадьба'), ('other', 'Другое')], max_length=100, null=True, verbose_name='Иконка'),
        ),
        migrations.AlterField(
            model_name='calendaritem',
            name='end',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.datetime(2024, 5, 3, 18, 0, 38, 131660, tzinfo=datetime.timezone.utc))], verbose_name='Конец'),
        ),
        migrations.AlterField(
            model_name='calendaritem',
            name='notification',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата уведомления'),
        ),
        migrations.AlterField(
            model_name='calendaritem',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now, validators=[django.core.validators.MinValueValidator(datetime.datetime(2024, 4, 5, 17, 0, 38, 131660, tzinfo=datetime.timezone.utc))], verbose_name='Начало'),
        ),
        migrations.AlterField(
            model_name='cloudfile',
            name='category',
            field=models.CharField(blank=True, choices=[('photo', 'Изображение'), ('doc', 'Документ'), ('archive', 'Архив'), ('video', 'Видео')], max_length=50, null=True),
        ),
    ]
