from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.decorators import ajax_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import Inventory_Form
from .models import Inventory,Inventory_time,Inventory_to_user
from .inventory import inventory_query
from celery.result import AsyncResult
from accounts.models import UserSettings
from actions.utils import create_action
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import datetime,time
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def inventory_submit(request):
#    print(UserSettings.objects.get(user=request.user).status)
#    if not UserSettings.objects.get(user=request.user).status in ABOVE_V1:
#        messages.success(request, '请购买VIP后继续使用网站功能.')
#        return redirect('/recharge')
    inventory_to_users = Inventory_to_user.objects.filter(user=request.user)
    inventorys = inventory_to_users.values_list('inventory', flat=True)
    inventorys = Inventory.objects.filter(id__in=inventorys)
    inventory = None
    inventory_time = None
    inventory_times = None
    inventory_to_user = False
    form = Inventory_Form(data=request.POST or None)
    if form.is_valid():
        user_setting= UserSettings.objects.filter(user=request.user)
        if user_setting[0].credit < 6:
            return redirect('/payment')
        new_asin = form.save(commit=False)
        if Inventory.objects.filter(asin=new_asin.asin,country=new_asin.country):
            inventory = Inventory.objects.filter(asin=new_asin.asin,country=new_asin.country)[0]
            inventory_times = Inventory_time.objects.filter(asin=inventory)
            inventory_time=Inventory_time.objects.filter(asin=inventory).first()
            if Inventory_to_user.objects.filter(inventory=inventory,user=request.user):
                inventory_to_user = True
        else:
            task = inventory_query.delay(new_asin.asin,new_asin.country)
            start = time.time()
            while AsyncResult(task.task_id).status != 'SUCCESS':
                if AsyncResult(task.task_id).status == 'FAILURE' or (time.time()-start)>40:
                    messages.success(request, '该ASIN不存在,请确认后重新查询.本次查询没有扣除积分.')
                    return redirect('/inventory')
                pass
            if AsyncResult(task.task_id).status == 'SUCCESS':
                #if not Inventory.objects.filter(asin=new_asin.asin,country=new_asin.country)[0].inventory_time.all().exists():
                #    Inventory.objects.filter(asin=new_asin.asin,country=new_asin.country)[0].delete()
                try:
                    inventory = Inventory.objects.filter(asin=new_asin.asin,country=new_asin.country)[0]
                    if inventory.inventory==0:
                        inventory.delete()
                        messages.success(request, '没有获得该ASIN的竞品信息,本次查询没有扣除积分.')
                        return redirect('/inventory')
                    else:
                        inventory_times = Inventory_time.objects.filter(asin=inventory)
                        inventory_time=Inventory_time.objects.filter(asin=inventory).first()
                    if Inventory_to_user.objects.filter(inventory=inventory,user=request.user):
                        inventory_to_user = True
                except:
                    messages.success(request, '没有获得该ASIN的竞品信息,本次查询没有扣除积分.')
                    return redirect('/inventory')
    paginator = Paginator(inventorys, 12)
    page = request.GET.get('page')
    try:
        inventorys_page = paginator.page(page)
    except PageNotAnInteger:
        inventorys_page = paginator.page(1)
    except EmptyPage:
        inventorys_page = paginator.page(paginator.num_pages)
    return render(request, 'crawler/inventory/inventory_submit.html', {'form': form,'inventorys': inventorys_page,
        'inventory_time':inventory_time,'inventory_to_user':inventory_to_user,'inventory': inventory,'inventory_times':inventory_times})


@ajax_required
@login_required
@require_POST
def add_monitor(request):
    inventory_id = request.POST.get('id') #id的用法
    inventory = Inventory.objects.filter(id=inventory_id)[0]
    if inventory and not Inventory_to_user.objects.filter(user=request.user,inventory=inventory):
        try:
            if Inventory_to_user.objects.filter(user=request.user).count()<36:
                inventory_to_user=Inventory_to_user(inventory=inventory,user=request.user,expired=timezone.now() + datetime.timedelta(days=31))
                inventory_to_user.save()
                if create_action(request.user, '跟踪了', inventory):
                    user_setting= UserSettings.objects.filter(user=request.user)
                    user_setting.update(credit=F('credit')-6)
                return JsonResponse({'status':'ok'}) #点击按钮后status是ok
        except:
            pass
    return JsonResponse({'status':'ko'}) #没点击按钮,status是ko


def more_monitor(request, id):
    inventory=get_object_or_404(Inventory, id=id)
    inventory_to_user=Inventory_to_user.objects.filter(inventory=inventory,user=request.user)
    days = (inventory_to_user[0].expired - datetime.datetime.now(timezone.utc)).days
    if days<92:
        if days>=0:
            inventory_to_user.update(expired=timezone.now()+datetime.timedelta(days=days+31))
        else:
            inventory_to_user.update(expired=timezone.now()+datetime.timedelta(days=31))
        messages.success(request, '%s已经续期一个月' % (inventory.text))
        if create_action(request.user, '续期了', inventory):
            user_setting=UserSettings.objects.filter(user=request.user)
            user_setting.update(credit=F('credit')-6)
        return redirect('/inventory/')
    else:
        messages.success(request, '%s的监控时间超过三个月,请不要继续续期' % (inventory.text))
        return redirect('/inventory/')


def delete(request, id):
    inventory=get_object_or_404(Inventory, id=id)
    if Inventory_to_user.objects.filter(inventory=inventory,user=request.user):
        Inventory_to_user.objects.filter(inventory=inventory,user=request.user).delete()
        messages.success(request, '已经删除%s' % (inventory.text))
        return redirect('/inventory/')