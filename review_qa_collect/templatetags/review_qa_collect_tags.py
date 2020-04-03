# -*- coding: utf-8 -*-
from django import template
from datetime import datetime, timezone
from ..models import Review_detail
# template.Library用来注册创建的template tags和filters
register = template.Library()




@register.assignment_tag
def reviews(product):
    return Review_detail.objects.filter(product=product)


@register.simple_tag
def count_reviews(product):
   return Review_detail.objects.filter(product=product).count()
