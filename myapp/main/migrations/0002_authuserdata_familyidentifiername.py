# Generated by Django 5.0.2 on 2024-03-03 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuserdata',
            name='familyIdentifierName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
