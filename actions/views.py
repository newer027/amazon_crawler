# -*- coding: utf-8 -*-
from .models import Action
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def action(request):
    actions=Action.objects.filter(user=request.user)

    paginator = Paginator(actions, 16)
    page = request.GET.get('page')
    try:
        actions_page = paginator.page(page)
    except PageNotAnInteger:
        actions_page = paginator.page(1)
    except EmptyPage:
        actions_page = paginator.page(paginator.num_pages)

    return render(request,'crawler/action/detail.html',
                              {'page': page,'actions': actions_page})

"""

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
"""