from django.shortcuts import render, get_object_or_404, redirect
from .forms import Product_Form
from .models import Product,Product_seller,Product_to_user,Seller_change
from .tasks import trigger_initial_task
#from celery.result import AsyncResult
from django.db.models import F
from accounts.models import UserSettings
from django.utils import timezone
from actions.utils import create_action
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.amazon_api import amazon_api
from keyword_rank.keyword_rank import find_item



@login_required
def product_submit(request):

    form = Product_Form(data=request.POST or None)
    if form.is_valid():
        user_setting= UserSettings.objects.filter(user=request.user)
        if user_setting[0].credit < 6:
            return redirect('/payment')
        if Product_to_user.objects.filter(user=request.user).count()>=36:
            messages.success(request, '因为网站资源有限,允许最多跟踪36条跟卖信息.您跟踪的跟卖信息已经达到36条.')
            return redirect('/follow_sale')

        new_asin = form.save(commit=False)
        if not Product.objects.filter(asin=new_asin.asin,country=new_asin.country):
            try:
                amazon = amazon_api(new_asin.country)
                item=find_item(amazon,new_asin.asin)
                new_asin.title = item['title']
                new_asin.img_url = item['img_url']
                new_asin.detail_page_url = item['detail_page_url']
                new_asin.save()
                trigger_initial_task.delay(new_asin.asin,new_asin.country)
            except:
                messages.success(request, '该ASIN不存在,请确认后重新查询.本次查询没有扣除积分.')
                return redirect('/follow_sale')
        product = Product.objects.filter(asin=new_asin.asin,country=new_asin.country)[0]
        #if Product.objects.filter(asin=new_asin.asin,country=new_asin.country):
            #product = Product.objects.filter(asin=new_asin.asin,country=new_asin.country)[0]
        if not Product_to_user.objects.filter(product=product,user=request.user):
            #print(product.text)
            product_to_user=Product_to_user(product=product,user=request.user,expired=timezone.now() + datetime.timedelta(days=31))
            product_to_user.save()
            if create_action(request.user, '跟踪了', product):
                user_setting.update(credit=F('credit')-6)
            messages.success(request, '网站开始为您跟踪跟卖信息,获取跟卖后会发送到您的邮箱.')
            return redirect('/follow_sale/')
            #return redirect(product.get_absolute_url())
        else:
            messages.success(request, '网站正在跟踪该跟卖信息.')
            return redirect('/follow_sale/')
            #while AsyncResult(task.task_id).status != 'SUCCESS':
            #    if AsyncResult(task.task_id).status == 'FAILURE':
            #        return redirect('/find_none')
            #    pass
            #if AsyncResult(task.task_id).status == 'SUCCESS':
            #product = Product.objects.filter(asin=new_asin.asin,country=new_asin.country)[0]

            #product_to_user=Product_to_user(product=product,user=request.user,expired=timezone.now() + datetime.timedelta(days=31))
            #product_to_user.save()
            #if create_action(request.user, '跟踪了:', product):
            #    user_setting.update(credit=F('credit')-4)
            #    return redirect(product.get_absolute_url())
            #if AsyncResult(task.task_id).status == 'FAILURE':
            #    return redirect('/find_none')

    product_to_users = Product_to_user.objects.filter(user=request.user)
    products = product_to_users.values_list('product', flat=True)
    products = Product.objects.filter(id__in=products)

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    return render(request, 'crawler/follow_sale/product_submit.html', {'form': form,'products': products_page,'page':page})


def more_monitor(request, id):
    product=get_object_or_404(Product, id=id)
    product_to_user=Product_to_user.objects.filter(product=product,user=request.user)
    days = (product_to_user[0].expired - datetime.datetime.now(timezone.utc)).days
    if days<92:
        if days>=0:
            product_to_user.update(expired=timezone.now()+datetime.timedelta(days=days+31))
        else:
            product_to_user.update(expired=timezone.now()+datetime.timedelta(days=31))
        messages.success(request, '%s已经续期一个月' % (product.text))
        if create_action(request.user, '续期了', product):
            user_setting=UserSettings.objects.filter(user=request.user)
            user_setting.update(credit=F('credit')-6)
        return redirect('/follow_sale/')
    else:
        messages.success(request, '%s的监控时间超过三个月,请不要继续续期' % (product.text))
        return redirect('/follow_sale/')


def delete(request, id):
    product=get_object_or_404(Product, id=id)
    if Product_to_user.objects.filter(product=product,user=request.user):
        Product_to_user.objects.filter(product=product,user=request.user).delete()
        messages.success(request, '已经删除%s' % (product.text))
        return redirect('/follow_sale/')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug)
    Product_sellers = Product_seller.objects.filter(product=product)
    seller_changes = Seller_change.objects.filter(product=product,status='new')
    return render(request, 'crawler/follow_sale/product_detail.html', {'product': product,'Product_sellers':Product_sellers,'seller_changes':seller_changes})
