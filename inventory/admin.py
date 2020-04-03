from django.contrib import admin
from .models import Inventory, Inventory_time, Inventory_to_user


class ModuleInline(admin.TabularInline):
    model = Inventory_time

@admin.register(Inventory)
class Inventory_Admin(admin.ModelAdmin):
    list_display = ['asin', 'title','created','img_url','detail_page_url','category']
    search_fields = ['title','asin']
    prepopulated_fields = {'slug': ('asin',)}
    inlines = [ModuleInline]


@admin.register(Inventory_to_user)
class Inventory_to_user_Admin(admin.ModelAdmin):
    list_display = ['inventory', 'user', 'created', 'expired']
    search_fields = ['inventory__asin','user__username']
