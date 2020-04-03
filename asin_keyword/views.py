from django.shortcuts import render, redirect
from .forms import Asin_keyword_Form
from .models import Asin_keyword
from .tasks import asin_to_keyword_task,delete_asin_keyword
from celery.result import AsyncResult
from django.db.models import F
from accounts.models import UserSettings
from actions.utils import create_action
from django.contrib.auth.decorators import login_required
import time, json
from django.http import HttpResponse
from core.decorators import ajax_required
from django.views.decorators.http import require_POST
from core.amazon_api import ABOVE_V1
from django.contrib import messages


@login_required
def asin_submit(request):
#    print(UserSettings.objects.get(user=request.user).status)
#    if not UserSettings.objects.get(user=request.user).status in ABOVE_V1:
#        messages.success(request, '请购买VIP后继续使用网站功能.')
#        return redirect('/recharge')

    asin_keyword = None
    asin_keywords = Asin_keyword.objects.all()
    asin_keywords = asin_keywords.order_by('-created')[:12]
    form = Asin_keyword_Form(data=request.POST or None)
    return render(request, 'crawler/asin_keyword/asin_submit.html', {'form': form,'asin_keywords': asin_keywords,'asin_keyword':asin_keyword})


@ajax_required
@login_required
@require_POST
def create_post(request):
    if request.method == 'POST':
        user_setting= UserSettings.objects.filter(user=request.user)
        if user_setting[0].credit < 4:
            return HttpResponse(
                        json.dumps({"response": "积分不够查询,请充值积分!"}),
                        content_type="application/json"
                    )

        asin = request.POST.get('asin')
        country = request.POST.get('country')
        response_data = {}


        if Asin_keyword.objects.filter(asin=asin,country=country):
            asin_keyword = Asin_keyword.objects.filter(asin=asin, country=country)[0]
            if create_action(request.user, '查询了', asin_keyword) and asin_keyword.keyword:
                user_setting.update(credit=F('credit')-4)
            response_data["asin"]= asin_keyword.asin
            response_data["title"]= asin_keyword.title
            response_data["keyword"]= asin_keyword.keyword
            response_data["img"]= asin_keyword.img
            response_data["url"]= asin_keyword.url
            response_data["country"]= asin_keyword.get_country_display()
            return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json")
        else:
            task = asin_to_keyword_task.delay(asin,country)
            start = time.time()
            while AsyncResult(task.task_id).status != 'SUCCESS':
                if AsyncResult(task.task_id).status == 'FAILURE' or (time.time()-start)>40:
                    return HttpResponse(
                        json.dumps({"response": "该ASIN不存在,请确认后重新查询.本次查询没有扣除积分."}),
                        content_type="application/json"
                    )
                pass
            if AsyncResult(task.task_id).status == 'SUCCESS':
                try:
                    if not Asin_keyword.objects.filter(asin=asin)[0].ean:
                        asin_keyword = Asin_keyword.objects.filter(asin=asin)[0]
                        delete_asin_keyword.delay(asin)
                        response_data["response"] = "无法查询该ASIN的Search Term，请填写正确的ASIN和正确的站点.（提醒：部分ASIN因亚马逊后台问题，无法查询Search Term）本次查询没有扣除积分."
                    else:
                        asin_keyword = Asin_keyword.objects.filter(asin=asin)[0]
                        if create_action(request.user, '查询了', asin_keyword) and asin_keyword.keyword:
                            user_setting.update(credit=F('credit')-4)
                    response_data["asin"]= asin_keyword.asin
                    response_data["title"]= asin_keyword.title
                    response_data["keyword"]= asin_keyword.keyword
                    response_data["img"]= asin_keyword.img
                    response_data["url"]= asin_keyword.url
                    response_data["country"]= asin_keyword.get_country_display()
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
                except:
                    return HttpResponse(
                        json.dumps({"response": "该ASIN不存在,请确认后重新查询.本次查询没有扣除积分."}),
                        content_type="application/json"
                    )

    else:
        return HttpResponse(
            json.dumps({"nothing to response": "data isn't valid"}),
            content_type="application/json"
        )

