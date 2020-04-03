# -*- coding: utf-8 -*-
from django import template
from core.models import Product_to_user
from django.contrib.auth.models import User
# template.Library用来注册创建的template tags和filters
register = template.Library()


@register.simple_tag
def latest_inven(user_id):
    return len(Product_to_user.objects.filter(user=User.objects.get(id=user_id),detail=True))
