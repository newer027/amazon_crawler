from django.contrib import admin
from .models import Asin_keyword


class Asin_keyword_Admin(admin.ModelAdmin):
    list_display = [
        'asin',
        'title',
        'ean',
        'keyword',
        'country',
    ]
    prepopulated_fields = {'slug': ('asin',)}

admin.site.register(Asin_keyword, Asin_keyword_Admin)
