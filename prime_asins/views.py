from django.shortcuts import render, redirect
from prime_asins.models import Asin_detail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from accounts.models import UserSettings
#from core.amazon_api import ABOVE_V1
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def asin_submit(request, country='us', category=None):
    #if not UserSettings.objects.get(user=request.user).status in ABOVE_V1:
    #    messages.success(request, '请购买VIP后继续使用网站功能.')
    #    return redirect('/recharge')
    asin_details = Asin_detail.objects.filter(country=country)
    asin_details = asin_details.order_by('description','sell_rank')

    countries = [country[0] for country in Asin_detail.COUNTRY_CHOICES]
    categories = [category[0] for category in Asin_detail.objects.filter(country=country).values_list('description').distinct('description')]

    if category:
        #asin_details = asin_details.filter(description__startswith=category)
        asin_details = asin_details.filter(description=category)

    paginator = Paginator(asin_details, 200)
    page = request.GET.get('page')
    try:
        asin_detail_page = paginator.page(page)
    except PageNotAnInteger:
        asin_detail_page = paginator.page(1)
    except EmptyPage:
        asin_detail_page = paginator.page(paginator.num_pages)

    return render(request, 'crawler/prime_asins/asin_submit.html', {'country':country,'countries':countries,'categories':categories,'category':category,'asin_details': asin_detail_page,})