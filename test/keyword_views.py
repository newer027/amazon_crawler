from django.shortcuts import render, get_object_or_404, redirect
from .forms import Asin_keyword_Form
from .models import Asin_keyword
from .tasks import asin_to_keyword_task
from django.contrib import messages
from celery.result import AsyncResult


def asin_submit(request):
    asin_keywords = Asin_keyword.objects.all()
    asin_keywords = asin_keywords.order_by('-created')[:12]
    form = Asin_keyword_Form(data=request.POST or None)
    if form.is_valid():
        new_asin = form.save(commit=False)
        try:
            if Asin_keyword.objects.filter(asin=new_asin.asin):
                asin_keyword = Asin_keyword.objects.filter(asin=new_asin.asin)[0]
                return redirect(asin_keyword.get_absolute_url())
            else:
                task = asin_to_keyword_task.delay(new_asin.asin)
                while AsyncResult(task.task_id).status != 'SUCCESS':
                    if AsyncResult(task.task_id).status == 'FAILURE':
                        return redirect('/find_none')
                        pass
                if AsyncResult(task.task_id).status == 'SUCCESS':
                    asin_keyword = Asin_keyword.objects.filter(asin=new_asin.asin)[0]
                    return redirect(asin_keyword.get_absolute_url())
                if AsyncResult(task.task_id).status == 'FAILURE':
                    return redirect('/find_none')
        except:
            messages.error(request, '对不起,这个ASIN并不存在')
    return render(request, 'crawler/asin_keyword/asin_submit.html', {'form': form,'asin_keywords': asin_keywords})


def asin_keyword(request, slug):
    asin_keyword = get_object_or_404(Asin_keyword, slug = slug)
    form = Asin_keyword_Form(data=request.POST or None)
    if form.is_valid():
        new_asin = form.save(commit=False)
        try:
            if Asin_keyword.objects.filter(asin=new_asin.asin):
                asin_keyword = Asin_keyword.objects.filter(asin=new_asin.asin)[0]
                return redirect(asin_keyword.get_absolute_url())
            else:
                task = asin_to_keyword_task.delay(new_asin.asin)
                while AsyncResult(task.task_id).status != 'SUCCESS':
                    if AsyncResult(task.task_id).status == 'FAILURE':
                        return redirect('/find_none')
                        pass
                if AsyncResult(task.task_id).status == 'SUCCESS':
                    asin_keyword = Asin_keyword.objects.filter(asin=new_asin.asin)[0]
                    return redirect(asin_keyword.get_absolute_url())
                if AsyncResult(task.task_id).status == 'FAILURE':
                    return redirect('/find_none')
        except:
            messages.error(request, '对不起,这个ASIN并不存在')
    return render(request, 'crawler/asin_keyword/asin_keyword.html', {'form': form,'asin_keyword': asin_keyword})
