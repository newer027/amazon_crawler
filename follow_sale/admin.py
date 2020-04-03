from django.contrib import admin
from .models import Product, Product_seller, Seller_change, Product_to_user


class ModuleInline(admin.TabularInline):
    model = Product_seller

@admin.register(Product)
class Product_Admin(admin.ModelAdmin):
    list_display = ['asin', 'title']
    search_fields = ['title','asin']
    prepopulated_fields = {'slug': ('asin',)}
    inlines = [ModuleInline]


class Seller_change_Admin(admin.ModelAdmin):
    list_display = [
        'product',
        'price',
        'status',
        'name',
        'sell_url',
        'seller_id',
        'created',
    ]

admin.site.register(Seller_change, Seller_change_Admin)


@admin.register(Product_to_user)
class Product_to_user_Admin(admin.ModelAdmin):
    list_display = ['product', 'user', 'created', 'expired']

class Product_seller_Admin(admin.ModelAdmin):
    list_display = [
        'product',
        'price',
        'name',
        'seller_id',
        'created',
    ]

admin.site.register(Product_seller, Product_seller_Admin)