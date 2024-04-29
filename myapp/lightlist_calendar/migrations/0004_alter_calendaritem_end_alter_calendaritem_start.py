# Generated by Django 5.0.3 on 2024-04-29 06:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightlist_calendar', '0003_alter_calendaritem_end_alter_calendaritem_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendaritem',
            name='end',
            field=models.DateTimeField(verbose_name='Конец'),
        ),
        migrations.AlterField(
            model_name='calendaritem',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Начало'),
        ),
    ]
