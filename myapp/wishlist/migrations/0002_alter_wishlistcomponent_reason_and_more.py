# Generated by Django 5.0.3 on 2024-04-29 06:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistcomponent',
            name='reason',
            field=models.CharField(choices=[('Новый год', 'Новый год'), ('Свадьба', 'Свадьба'), ('День рождения', 'День Рождения'), ('8 марта', '8 Марта'), ('23 февраля', '23 Февраля'), ('Другое', 'Другое')], default='Другое', max_length=100, null=True, verbose_name='Причина'),
        ),
        migrations.AlterField(
            model_name='wishlistcomponent',
            name='wish_picture',
            field=models.ImageField(blank=True, null=True, upload_to='wishImg/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico', 'jpeg', 'webp'])], verbose_name='Картинка'),
        ),
    ]