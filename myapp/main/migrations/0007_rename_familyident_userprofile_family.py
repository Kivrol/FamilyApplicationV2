# Generated by Django 5.0.2 on 2024-03-09 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_family_avatar_remove_userprofile_avatar_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='familyIdent',
            new_name='family',
        ),
    ]
