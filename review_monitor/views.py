from django.shortcuts import render, get_object_or_404, redirect
from .forms import Product_Form
from .models import Product,Review
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
from core.amazon_api import ABOVE_V1


@login_required
def product_submit(request):
#    print(UserSettings.objects.get(user=request.user).status)
#    if not UserSettings.objects.get(user=request.user).status in ABOVE_V1:
#        messages.success(request, '请购买VIP后继续使用网站功能.')
#        return redirect('/recharge')

    form = Product_Form(data=request.POST or None)
    if form.is_valid():
        user_setting= UserSettings.objects.filter(user=request.user)
        if user_setting[0].credit < 6:
            return redirect('/payment')
        if Product.objects.filter(user=request.user).count()>=36:
            messages.success(request, '因为网站资源有限,允许最多跟踪36条差评信息.您跟踪的差评信息已经达到36条.')
            return redirect('/review_monitor')

        new_asin = form.save(commit=False)
        if not Product.objects.filter(asin=new_asin.asin,country=new_asin.country,user=request.user):
            try:
                amazon = amazon_api(new_asin.country)
                item=find_item(amazon,new_asin.asin)
                new_asin.title = item['title']
                new_asin.img_url = item['img_url']
                new_asin.detail_page_url = item['detail_page_url']
                new_asin.star=new_asin.star
                new_asin.user=request.user
                new_asin.expired=timezone.now() + datetime.timedelta(days=31)
                new_asin.save()
            except:
                messages.success(request, '该ASIN不存在,请确认后重新查询.本次查询没有扣除积分.')
                return redirect('/review_monitor')
            product = Product.objects.filter(asin=new_asin.asin,country=new_asin.country)[0]
            trigger_initial_task.delay(new_asin.asin,new_asin.country,new_asin.star)
            if create_action(request.user, '跟踪了', product):
                user_setting.update(credit=F('credit')-6)
            messages.success(request, '网站开始为您跟踪跟卖信息,获取跟卖后会发送到您的邮箱.')
        else:
            messages.success(request, '网站正在跟踪该跟卖信息.')
        return redirect('/review_monitor/')

    products = Product.objects.filter(user=request.user)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    return render(request, 'crawler/review_monitor/product_submit.html', {'form': form,'products': products_page,'page':page})


def more_monitor(request, id):
    product=Product.objects.filter(id=id)
    days = (product[0].expired - datetime.datetime.now(timezone.utc)).days
    if days<92:
        if days>=0:
            product.update(expired=timezone.now()+datetime.timedelta(days=days+31))
        else:
            product.update(expired=timezone.now()+datetime.timedelta(days=31))
        messages.success(request, '%s已经续期一个月' % (product[0].text))
        if create_action(request.user, '续期了', product[0]):
            user_setting=UserSettings.objects.filter(user=request.user)
            user_setting.update(credit=F('credit')-6)
        return redirect('/review_monitor/')
    else:
        messages.success(request, '%s的监控时间超过三个月,请不要继续续期' % (product[0].text))
        return redirect('/review_monitor/')


def delete(request, id):
    product=get_object_or_404(Product, id=id)
    if product.user==request.user:
        product.delete()
        messages.success(request, '已经删除%s' % (product.text))
        return redirect('/review_monitor/')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug)
    reviews = Review.objects.filter(product=product)
    return render(request, 'crawler/review_monitor/product_detail.html', {'product': product,'reviews':reviews})
