from django.contrib import admin
from .models import Url_to_wishlist


class Url_to_wishlist_Admin(admin.ModelAdmin):
    list_display = [
        'url',
        'add',
    ]


admin.site.register(Url_to_wishlist, Url_to_wishlist_Admin)