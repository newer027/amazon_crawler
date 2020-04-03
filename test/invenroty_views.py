from django.shortcuts import render, get_object_or_404, redirect
from .forms import Inventory_Form
from .models import Inventory,Inventory_time
from .tasks import inventory_query_task
#from amazon.api import AmazonAPI
from django.contrib import messages
#from datetime import datetime
from celery.result import AsyncResult
#import time


def inventory_submit(request):
    inventorys = Inventory.objects.all()
    inventorys = inventorys.order_by('-created')[:12]
    form = Inventory_Form(data=request.POST or None)
    if form.is_valid():
        new_asin = form.save(commit=False)
        try:
            if Inventory.objects.filter(asin=new_asin.asin):
                inventory = Inventory.objects.filter(asin=new_asin.asin)[0]
                return redirect(inventory.get_absolute_url())
            else:
                task = inventory_query_task.delay(new_asin.asin)
                while AsyncResult(task.task_id).status != 'SUCCESS':
                    if AsyncResult(task.task_id).status == 'FAILURE':
                        return redirect('/find_none')
                        pass
                if AsyncResult(task.task_id).status == 'SUCCESS':
                    inventory = Inventory.objects.filter(asin=new_asin.asin)[0]
                    return redirect(inventory.get_absolute_url())
                if AsyncResult(task.task_id).status == 'FAILURE':
                    return redirect('/find_none')
        except:
            messages.error(request, '对不起,这个ASIN并不存在')
    return render(request, 'crawler/inventory/inventory_submit.html', {'form': form,'inventorys': inventorys})


def asin_inventory(request, slug):
    inventory = get_object_or_404(Inventory, slug = slug)
    inventory_times = Inventory_time.objects.filter(asin=inventory)
    form = Inventory_Form(data=request.POST or None)
    if form.is_valid():
        new_asin = form.save(commit=False)
        try:
            if Inventory.objects.filter(asin=new_asin.asin):
                inventory = Inventory.objects.filter(asin=new_asin.asin)[0]
                return redirect(inventory.get_absolute_url())
            else:
                task = inventory_query_task.delay(new_asin.asin)
                while AsyncResult(task.task_id).status != 'SUCCESS':
                    if AsyncResult(task.task_id).status == 'FAILURE':
                        return redirect('/find_none')
                        pass
                if AsyncResult(task.task_id).status == 'SUCCESS':
                    inventory = Inventory.objects.filter(asin=new_asin.asin)[0]
                    return redirect(inventory.get_absolute_url())
                if AsyncResult(task.task_id).status == 'FAILURE':
                    return redirect('/find_none')
        except:
            messages.error(request, '对不起,这个ASIN并不存在')
    return render(request, 'crawler/inventory/asin_inventory.html', {'form': form,'inventory': inventory,'inventory_times':inventory_times})