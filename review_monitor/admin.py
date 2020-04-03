from django.contrib import admin
from .models import Product, Review


class ModuleInline(admin.TabularInline):
    model = Review


@admin.register(Product)
class Product_Admin(admin.ModelAdmin):
    list_display = ['asin', 'title','user', 'created', 'expired',]
    prepopulated_fields = {'slug': ('asin',)}
    search_fields = ['title','asin']
    inlines = [ModuleInline]