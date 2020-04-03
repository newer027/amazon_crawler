from django.contrib import admin

from .models import UserSettings


class UserSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'credit',
        'modified',
        'created',
    ]


admin.site.register(UserSettings, UserSettingsAdmin)
