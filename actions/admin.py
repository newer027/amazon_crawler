# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Action
from daterange_filter.filter import DateRangeFilter


class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target_text', 'created',)
    list_filter = (('created',DateRangeFilter),)
    search_fields = ('verb', 'user__username', 'target_text',)

#注册action
admin.site.register(Action, ActionAdmin)
