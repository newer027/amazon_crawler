#-*- coding:utf-8 -*-

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from payment.config import settings
from alipay import Alipay
from .models import Bill
import urllib
from accounts.models import UserSettings
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from actions.utils import create_action
from asin_keyword.emails import send_email
from short_url.shorten_url import get_short_code
from django.http import HttpResponse
#import datetime


alipay = Alipay(pid=settings.ALIPAY_PARTNER, key=settings.ALIPAY_KEY, seller_email=settings.ALIPAY_SELLER_EMAIL)

def buy_credit(user, credit,request):
    user.update(credit=F('credit')+credit)
    create_action(request.user, '购买了%s积分' % (credit))

@login_required
def upgrade_account(request, add_credit):

    user = request.user
    try:
        bill = user.bill
    except:
        bill = Bill(user=user)
    tn = get_short_code()
    bill.tn=tn
    bill.save()

    if add_credit == "bronze":
        bill.add_credit = 100
        bill.save()
        url=alipay.create_direct_pay_by_user_url(out_trade_no=tn, subject=u'获得积分',total_fee='100.00',
                                    return_url=settings.ALIPAY_RETURN_URL, notify_url=settings.ALIPAY_NOTIFY_URL)
        return redirect (url)
    else:
        return redirect ('/recharge/payment_error')


def return_url_handler (request):
    user_setting= UserSettings.objects.filter(user=request.user)
    GET=request.GET.copy()
    GET = GET.dict()
    if alipay.verify_notify (**GET):
        if True:
            tn = request.GET.get('out_trade_no')
            bill = Bill.objects.get (tn=tn)
            trade_status = request.GET.get('trade_status')
            if trade_status=='TRADE_SUCCESS' and bill.user==request.user:
                bill.trade_status = trade_status
                bill.save()
                buy_credit(user_setting, 100,request)
            return redirect ('/recharge/success')
    return redirect ('/recharge/error')


def notify_url_handler (request):
    if request.method == 'POST':
        #if notify_verify (request.POST):
        user_setting= UserSettings.objects.filter(user=request.user)[0]
        if True:
            tn = request.POST.get('out_trade_no')
            bill = Bill.objects.get (tn=tn)
            trade_status = request.POST.get('trade_status')
            if trade_status=='TRADE_SUCCESS' and bill.user==request.user:
                return HttpResponse("success")
    return HttpResponse("fail")
