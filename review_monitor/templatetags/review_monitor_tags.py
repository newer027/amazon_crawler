# -*- coding: utf-8 -*-
from django import template
from datetime import datetime, timezone
from ..models import Review
# template.Library用来注册创建的template tags和filters
register = template.Library()


@register.assignment_tag
def days_remain(product,user):
    days = (product.expired - datetime.now(timezone.utc)).days
    if days<0:
        days=0
    return days


@register.assignment_tag
def reviews(product):
    return Review.objects.filter(product=product)


@register.simple_tag
def count_reviews(product):
   return Review.objects.filter(product=product).count()