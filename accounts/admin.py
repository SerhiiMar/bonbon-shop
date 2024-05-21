from django.contrib import admin

from accounts import models


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    pass
