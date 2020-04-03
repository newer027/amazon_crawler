from django.contrib import admin
from .models import Keyword_rank, Rank, Rank_to_user



"""
class Keyword_rank_Admin(admin.ModelAdmin):
    list_display = [
        'date',
        'asin',
        'title',
    ]

    list_filter = [
        'date',
        'title',
    ]


class Rank_Admin(admin.ModelAdmin):
    list_display = [
        'keyword',
        'page',
        'number',
    ]


admin.site.register(Keyword_rank, Keyword_rank_Admin)
admin.site.register(Rank, Rank_Admin)

"""
class ModuleInline(admin.TabularInline):
    model = Rank


@admin.register(Keyword_rank)
class Keyword_rank_Admin(admin.ModelAdmin):
    list_display = ['asin', 'title', 'word', 'country']
    search_fields = ['asin','title', 'word']
    prepopulated_fields = {'slug': ('asin',)}
    inlines = [ModuleInline]


@admin.register(Rank_to_user)
class Rank_to_user_Admin(admin.ModelAdmin):
    list_display = ['keyword_rank', 'user']
    search_fields = ['keyword_rank','user__username']