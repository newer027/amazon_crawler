from django.shortcuts import render, redirect
from .forms import Asin_detail_Form
from core.models import Product,Product_to_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import UserSettings
from core.amazon_api import ABOVE_V1
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def asin_submit(request):
#    if not UserSettings.objects.get(user=request.user).status in ABOVE_V1:
#        messages.success(request, '请购买VIP后继续使用网站功能.')
#        return redirect('/recharge')

    detail_to_user = Product_to_user.objects.filter(user=request.user,detail=True)
    asin_details = detail_to_user.values_list('asin', flat=True)
    asin_details = Product.objects.filter(id__in=asin_details)

    form = Asin_detail_Form()
    if 'asins_in' in request.POST:
        form = Asin_detail_Form(data=request.POST or None)
        print(request.POST,form.is_valid())
        if form.is_valid():
            new_asin = form.save(commit=False)
            for asin in new_asin.asins_in.splitlines():
                if not Product.objects.filter(asin=asin,country=new_asin.country,detail=True):
                    if Product.objects.filter(asin=asin,country=new_asin.country):
                        product=Product.objects.filter(asin=asin,country=new_asin.country)[0]
                        product.detail=True
                        product.save()
                    else:
                        product=Product(asin=asin,country=new_asin.country,detail=True)
                        product.save()
                    if not Product_to_user.objects.filter(asin=product,user=request.user,detail=True):
                        detail_to_user=Product_to_user(asin=product,user=request.user,detail=True)
                        detail_to_user.save()
                else:
                    product=Product.objects.get(asin=asin,country=new_asin.country,detail=True)
                    if not Product_to_user.objects.filter(asin=product,user=request.user,detail=True):
                        if Product_to_user.objects.filter(asin=product,user=request.user):
                            detail_to_user=Product_to_user.objects.get(asin=product,user=request.user)
                            detail_to_user.detail=True
                            detail_to_user.save()
                        else:
                            detail_to_user=Product_to_user(asin=product,user=request.user,detail=True)
                            detail_to_user.save()

            messages.success(request, '查询任务已经保存,稍后开始为您查询.')
            return redirect('/asin_detail/')
    elif 'delete' in request.POST:
        products=Product.objects.filter(pk__in=request.POST.getlist('delete'))
        Product_to_user.objects.filter(asin__in=products,user=request.user).prefetch_related().update(detail=False)
        return redirect('/asin_detail/')

    paginator = Paginator(asin_details, 200)
    page = request.GET.get('page')
    try:
        asin_detail_page = paginator.page(page)
    except PageNotAnInteger:
        asin_detail_page = paginator.page(1)
    except EmptyPage:
        asin_detail_page = paginator.page(paginator.num_pages)

    return render(request, 'crawler/asin_detail/asin_submit.html', {'form':form,'asin_details': asin_detail_page,})
