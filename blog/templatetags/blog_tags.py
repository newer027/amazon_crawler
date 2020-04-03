# -*- coding: utf-8 -*-
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

# template.Library用来注册创建的template tags和filters
register = template.Library()

from ..models import Blog

# Post.published的数量
@register.simple_tag
def total_posts():
    return Blog.published.count()


# published时间逆序,得到最新的5个post
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Blog.published.order_by('-publish')[:count]
    # latest_posts.html中 'latest_posts'来自上面计算得到的latest_posts
    return {'latest_posts': latest_posts}


# annotate用来提取评论最多的5个post
@register.assignment_tag
def get_most_commented_posts(count=5):
    return Blog.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


# markdown的作用
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
