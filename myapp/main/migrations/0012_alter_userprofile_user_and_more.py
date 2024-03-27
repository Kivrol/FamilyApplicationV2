# Generated by Django 5.0.3 on 2024-03-27 17:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_joinfamilyrequest_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wishlistcomponent',
            name='custom_reason',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Своя причина'),
        ),
        migrations.AlterField(
            model_name='wishlistcomponent',
            name='reason',
            field=models.CharField(choices=[('нг', 'Новый год'), ('св', 'Свадьба'), ('др', 'День Рождения'), ('wd', '8 Марта'), ('md', '23 Февраля'), ('др', 'Другое')], default='другое', max_length=100, null=True, verbose_name='Причина'),
        ),
        migrations.CreateModel(
            name='CloudFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='files/')),
                ('category', models.CharField(blank=True, choices=[('img', 'Изображение'), ('doc', 'Документ'), ('archive', 'Архив'), ('video', 'Видео')], max_length=50, null=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.family')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
