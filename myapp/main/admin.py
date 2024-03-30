from django.contrib import admin
from . import models


@admin.register(models.UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('user', 'phoneNumber', 'birthDate', 'patronimic', 'profileAvatar')
    list_display_links = ('user',)


# @admin.register(models.AuthUserData)
# class AuthUserAdmin(admin.ModelAdmin):
#     list_display = ('userName', 'password', 'email', 'phoneNumber', 'birthDate', 'joinDate', 'name', 'surname', 'patronimic', 'avatar')
#     list_display_links = ('userName',)


admin.site.register(models.Family)
admin.site.register(models.JoinFamilyRequest)
admin.site.register(models.ProductListComponent)
admin.site.register(models.WishListComponent)
admin.site.register(models.CloudFile)
admin.site.register(models.CalendarItem)
