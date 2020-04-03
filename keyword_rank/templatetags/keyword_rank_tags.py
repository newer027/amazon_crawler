# -*- coding: utf-8 -*-
from django import template
from datetime import datetime, timezone
from ..models import Rank
# template.Library用来注册创建的template tags和filters
register = template.Library()


@register.assignment_tag
def days_remain(keyword_rank,user):
    rank_to_user = keyword_rank.rank_to_user.filter(user=user)[0]
    days = (rank_to_user.expired - datetime.now(timezone.utc)).days
    if days<0:
        days=0
    return days


@register.simple_tag
def latest_rank(keyword_rank):
    if Rank.objects.filter(keyword_rank=keyword_rank):
        return Rank.objects.filter(keyword_rank=keyword_rank).first().text
    else:
        return None


@register.assignment_tag
def rank_times(keyword_rank):
    return Rank.objects.filter(keyword_rank=keyword_rank)