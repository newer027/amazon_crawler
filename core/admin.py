from django.contrib import admin
from .models import Product


class Product_Admin(admin.ModelAdmin):
    list_display = [
        'asin',
        'title',
    ]

admin.site.register(Product, Product_Admin)
