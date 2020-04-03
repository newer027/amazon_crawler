from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,redirect
from short_url.models import Shorten_Url
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from accounts.models import UserSettings
import time, re


def index(request):
    return render(
        request,
        'crawler/index.html',
    )


def redirect_original(request, shorten_id):
    url = get_object_or_404(Shorten_Url, shorten_id=shorten_id) # get object, if not found return 404 error
    url.count += 1
    url.save()
    qid=str(int(time.time()))
    return HttpResponseRedirect(re.sub(r'\d{10}',qid,url.httpurl))


def recharge(request):
    return render(
        request,
        'crawler/recharge.html',
    )


def find_none(request):
    return render(
        request,
        'crawler/find_none.html',
    )

def converter(request):
    return render(
        request,
        'crawler/converter.html',
    )

@login_required
def check(request):
    user_setting= UserSettings.objects.filter(user=request.user)
    if user_setting[0].checked:
        messages.error(request, '请不要重复签到.')
        return redirect('/')
    else:
        user_setting.update(checked=True)
        user_setting.update(credit=F('credit')+100)
        messages.success(request, '已经签到,您获得了100积分的奖励.')
        return redirect('/')
