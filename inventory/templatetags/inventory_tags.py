# -*- coding: utf-8 -*-
from django import template
from datetime import datetime, timezone
from ..models import Inventory_time
# template.Library用来注册创建的template tags和filters
register = template.Library()


@register.assignment_tag
def days_remain(inventory,user):
    inventory_to_user = inventory.inventory_to_user.filter(user=user)[0]
    days = (inventory_to_user.expired - datetime.now(timezone.utc)).days
    if days <0:
        days =0
    return days


@register.assignment_tag
def inven_time(inventory):
    return Inventory_time.objects.filter(asin=inventory)


@register.simple_tag
def latest_inven(inventory):
    if Inventory_time.objects.filter(asin=inventory):
        return Inventory_time.objects.filter(asin=inventory).first().inventory
    else:
        return None