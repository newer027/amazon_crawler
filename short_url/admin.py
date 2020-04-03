from django.contrib import admin
from .models import Shorten_Url
# Register your models here.

class UrlsAdmin(admin.ModelAdmin):
    list_display = ('shorten_id','httpurl','pub_date', 'count','asin','seller','country','keywords')
    ordering = ('-pub_date',)

admin.site.register(Shorten_Url, UrlsAdmin) # Register the Urls model with UrlsAdmin options
