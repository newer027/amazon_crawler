from django.shortcuts import render, get_object_or_404,redirect
from .forms import Shorten_Url_Form
from .models import Shorten_Url
from .shorten_url import create_url
from django.contrib import messages
from actions.utils import create_action
from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required


@login_required
def url_submit(request):
    form = Shorten_Url_Form(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_url=form.save(commit=False)
            task = create_url.delay(new_url.asin,new_url.country,new_url.seller,request.user.id,new_url.keywords.splitlines())
            while AsyncResult(task.task_id).status != 'SUCCESS':
                if AsyncResult(task.task_id).status == 'FAILURE':
                    messages.success(request, '发生网络错误,请稍后再次查询.')
                    return redirect('/short_url')
                pass
            if AsyncResult(task.task_id).status == 'SUCCESS':
                create_action(request.user, '创建了', Shorten_Url.objects.first())
                return redirect('/short_url')

    urls = Shorten_Url.objects.filter(user=request.user)
    return render(request, 'crawler/short_url/url_submit.html', {'form':form, 'urls': urls})


def url_detail(request,id):
    url = get_object_or_404(Shorten_Url, id = id)
    return render(request, 'crawler/short_url/url_detail.html', {'url': url})


def delete(request, id):
    get_object_or_404(Shorten_Url, id=id).delete()
    return redirect('/short_url')

"""
if form.is_valid():
    new_url = form.save(commit=False)
    if Urls.objects.filter(httpurl=new_url.httpurl):
        url = Urls.objects.filter(httpurl=new_url.httpurl)
        return redirect(url.get_absolute_url())
    else:
        new_url.short_id = get_short_code()
        new_url.save()
        return redirect(new_url.get_absolute_url())
"""
