# -*- coding: utf-8 -*-
from django import template
from datetime import datetime, timezone
from ..models import Seller_change,Product_seller
# template.Library用来注册创建的template tags和filters
register = template.Library()


@register.assignment_tag
def days_remain(product,user):
    product_to_user = product.product_to_user.filter(user=user)[0]
    days = (product_to_user.expired - datetime.now(timezone.utc)).days
    if days<0:
        days=0
    return days


@register.assignment_tag
def seller_change(product):
    return Seller_change.objects.filter(product=product,status='new')


@register.assignment_tag
def product_seller(product):
    return Product_seller.objects.filter(product=product)


@register.simple_tag
def count_change(product):
   return Seller_change.objects.filter(product=product,status='new').count()