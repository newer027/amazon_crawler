from datetime import datetime

from django import forms
from django.contrib import admin

from redactor.widgets import RedactorEditor

from .models import Blog, BlogAd


class BlogAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'modified')
    list_display = ('title', 'author', 'status', 'date_published', 'created',
                    'modified')
    list_filter = ('status', 'author')
    search_fields = (
        'title',
        'Content',
    )

    fieldsets = (
        ('', {
            'fields': ('status', 'author',)
        }),
        ('Content', {
            'fields': ('title', 'slug', 'content','date_published')
        }),
    )


class BlogAdAdmin(admin.ModelAdmin):
    list_display = ('description', 'position', 'created', 'modified')


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogAd, BlogAdAdmin)
