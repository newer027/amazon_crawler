from django.shortcuts import render, get_object_or_404, redirect
from .forms import Product_Form
from core.models import Product,Product_to_user
from .models import Review_detail, QA_detail
from accounts.models import UserSettings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.amazon_api import ABOVE_V1
from django.utils import timezone
import csv,time,codecs
from django.http import HttpResponse


@login_required
def product_submit(request):
    #if not UserSettings.objects.get(user=request.user).status in ABOVE_V1:
    #    messages.success(request, '请购买VIP后继续使用网站功能.')
    #    return redirect('/recharge')

    form = Product_Form(data=request.POST or None)
    if form.is_valid():
        new_asin = form.save(commit=False)
        overflow=False
        for asin in new_asin.asins_in.splitlines():
            if len(Product_to_user.objects.filter(user=request.user,review_qa=True))>4:
                overflow=True
            else:
                if not Product.objects.filter(asin=asin,country=new_asin.country,review_qa=True):
                    if Product.objects.filter(asin=asin,country=new_asin.country):
                        product=Product.objects.filter(asin=asin,country=new_asin.country)[0]
                        product.review_qa=True
                        product.review_qa_apply_time=timezone.now()
                        product.save()
                    else:
                        product=Product(asin=asin,country=new_asin.country,review_qa_apply_time=timezone.now(),review_qa=True)
                        product.save()
                    if not Product_to_user.objects.filter(asin=product,user=request.user,review_qa=True):
                        detail_to_user=Product_to_user(asin=product,user=request.user,review_qa=True)
                        detail_to_user.save()
                else:
                    product=Product.objects.get(asin=asin,country=new_asin.country,review_qa=True)
                    if not Product_to_user.objects.filter(asin=product,user=request.user,review_qa=True):
                        if Product_to_user.objects.filter(asin=product,user=request.user):
                            detail_to_user=Product_to_user.objects.get(asin=product,user=request.user)
                            detail_to_user.review_qa=True
                            detail_to_user.save()
                        else:
                            detail_to_user=Product_to_user(asin=product,user=request.user,review_qa=True)
                            detail_to_user.save()
        if overflow:
            messages.success(request, '抓取评论和问答的服务处于试用期,每个用户最多采集五个ASIN.')
        else:
            messages.success(request, '查询任务已经保存,稍后开始为您查询.')
        return redirect('/review_qa_collect')

    product_to_user = Product_to_user.objects.filter(user=request.user,review_qa=True)
    products = product_to_user.values_list('asin', flat=True)
    products = Product.objects.filter(id__in=products)

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    return render(request, 'crawler/review_qa_collect/product_submit.html', {'form': form,'products': products_page,'page':page})


def delete(request, id):
    product=get_object_or_404(Product, id=id)
    Product_to_user.objects.filter(asin=product,user=request.user).prefetch_related().update(review_qa=False)
    messages.success(request, '已经删除%s' % (product.text))
    return redirect('/review_qa_collect/')


def product_detail(request, re_qa_slug):
    product = get_object_or_404(Product, re_qa_slug = re_qa_slug)
    reviews = Review_detail.objects.filter(product=product)
    QAs = QA_detail.objects.filter(product=product)

    paginator = Paginator(reviews, 20)
    page = request.GET.get('page')
    try:
        reviews_page = paginator.page(page)
    except PageNotAnInteger:
        reviews_page = paginator.page(1)
    except EmptyPage:
        reviews_page = paginator.page(paginator.num_pages)
    return render(request, 'crawler/review_qa_collect/product_detail.html', {'product': product,'reviews':reviews_page,'page':page,'QAs':QAs})


def qa_csv_view(request,pk):
    FILENAME_DATE_FORMAT = '%Y_%m_%d'
    product=get_object_or_404(Product, pk=pk)
    data = QA_detail.objects.filter(product=product)
    response = HttpResponse(content_type='text/csv')
    attachment_filename = '%s %s Question_Answer %s.csv' % (product.country,product.asin,time.strftime(FILENAME_DATE_FORMAT,time.gmtime()))
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename='+attachment_filename
    headers = ['回答日期', '问题', '答案', '回答人','VOTE数量','答案总数','所有答案链接']
    writer = csv.writer(response)
    writer.writerow(headers)
    for item in data:
        row = [
            item.qa_time,
            item.question,
            item.answer,
            item.answer_person,
            item.vote,
            item.num,
            item.answer_url,
        ]
        writer.writerow(row)
    return response

def review_csv_view(request,pk):
    FILENAME_DATE_FORMAT = '%Y_%m_%d'
    DATE_FORMAT = '%m/%d/%Y'
    product=get_object_or_404(Product, pk=pk)
    data = Review_detail.objects.filter(product=product)
    response = HttpResponse(content_type='text/csv')
    attachment_filename = '%s %s Review %s.csv' % (product.country,product.asin,time.strftime(FILENAME_DATE_FORMAT,time.gmtime()))
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename='+attachment_filename
    headers = ['采集日期', '品牌', '星级', 'ASIN','买家ID','买家URL','评论日期','评论内容','中文翻译','是否优惠购买']
    writer = csv.writer(response)
    writer.writerow(headers)

    for item in data:
        if item.normal:
            vp="真实购买"
        else:
            vp="直接评论"
        row = [
            product.created.strftime(DATE_FORMAT),
            product.brand,
            item.star,
            product.asin,
            item.customer_id,
            item.customer_url,
            item.review_time,
            item.review_text,
            item.review_chinese,
            vp,
        ]
        writer.writerow(row)
    return response