# Generated by Django 5.0.2 on 2024-05-11 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_alter_wishlistcomponent_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistcomponent',
            name='custom_reason',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание'),
        ),
    ]