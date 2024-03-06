from django.contrib import admin
from . import models

@admin.register(models.UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('phoneNumber', 'birthDate', 'patronimic', 'avatar')
    list_display_links = ('phoneNumber',)


# @admin.register(models.AuthUserData)
# class AuthUserAdmin(admin.ModelAdmin):
#     list_display = ('userName', 'password', 'email', 'phoneNumber', 'birthDate', 'joinDate', 'name', 'surname', 'patronimic', 'avatar')
#     list_display_links = ('userName',)
