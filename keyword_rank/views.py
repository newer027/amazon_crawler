from django.shortcuts import render, get_object_or_404,redirect
from .forms import Keyword_rank_Form
from .models import Keyword_rank, Rank_to_user
from .keyword_rank import find_item, rank_in_web
from core.amazon_api import amazon_api
from django.db.models import F
from accounts.models import UserSettings
from django.utils import timezone
from actions.utils import create_action
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from core.amazon_api import ABOVE_V1


@login_required
def keyword_list(request):
    #print(UserSettings.objects.get(user=request.user).status)
    #if not UserSettings.objects.get(user=request.user).status in ABOVE_V1:
    #    messages.success(request, '请购买VIP后继续使用网站功能.')
    #    return redirect('/recharge')

    rank_to_users = Rank_to_user.objects.filter(user=request.user)
    keyword_ranks = rank_to_users.values_list('keyword_rank', flat=True)
    keyword_ranks = Keyword_rank.objects.filter(id__in=keyword_ranks)

    form = Keyword_rank_Form()
    if 'word' in request.POST:
        form = Keyword_rank_Form(data=request.POST or None)
        if form.is_valid():
            user_setting= UserSettings.objects.filter(user=request.user)
            if user_setting[0].credit < 6:
                return redirect('/recharge')
            if Rank_to_user.objects.filter(user=request.user).count()>=36:
                messages.success(request, '因为网站资源有限,允许最多跟踪36条排名信息.您跟踪的排名信息已经达到36条.')
                return redirect('/keyword_rank')


            new_asin = form.save(commit=False)
            if not Keyword_rank.objects.filter(asin=new_asin.asin,country=new_asin.country,word=new_asin.word):
                try:
                    amazon = amazon_api(new_asin.country)
                    item=find_item(amazon,new_asin.asin)
                    new_asin.title = item['title']
                    new_asin.img_url = item['img_url']
                    new_asin.detail_page_url = item['detail_page_url']
                    new_asin.save()
                    rank_in_web.delay(new_asin.asin,new_asin.word,new_asin.country)
                except:
                    messages.success(request, '该ASIN不存在,请确认后重新查询.本次查询没有扣除积分.')
                    return redirect('/keyword_rank')
            keyword_rank = Keyword_rank.objects.filter(asin=new_asin.asin,word=new_asin.word,country=new_asin.country)[0]
            if not Rank_to_user.objects.filter(keyword_rank=keyword_rank,user=request.user):
                rank_to_user=Rank_to_user(keyword_rank=keyword_rank,user=request.user,expired=timezone.now() + datetime.timedelta(days=31))
                rank_to_user.save()
                if create_action(request.user, '跟踪了', keyword_rank):
                    user_setting.update(credit=F('credit')-6)
                messages.success(request, '网站开始为您跟踪排名信息.')
                return redirect('/keyword_rank/')
            else:
                messages.success(request, '网站正在跟踪该排名信息.')
                return redirect('/keyword_rank/')
    elif 'asin_filter' in request.POST:
        print(request.POST.lists())
        keyword_ranks=keyword_ranks.filter(asin=request.POST['asin_filter'])

    paginator = Paginator(keyword_ranks, 12)
    page = request.GET.get('page')
    try:
        keyword_ranks_page = paginator.page(page)
    except PageNotAnInteger:
        keyword_ranks_page = paginator.page(1)
    except EmptyPage:
        keyword_ranks_page = paginator.page(paginator.num_pages)
    return render(request, 'crawler/keyword_rank/keyword_list.html', {'form':form, 'keyword_ranks': keyword_ranks_page})


def more_monitor(request, id):
    keyword_rank=get_object_or_404(Keyword_rank, id=id)
    rank_to_user=Rank_to_user.objects.filter(keyword_rank=keyword_rank,user=request.user)
    days = (rank_to_user[0].expired - datetime.datetime.now(timezone.utc)).days
    if days<92:
        if days>=0:
            rank_to_user.update(expired=timezone.now()+datetime.timedelta(days=days+31))
        else:
            rank_to_user.update(expired=timezone.now()+datetime.timedelta(days=31))
        messages.success(request, '%s已经续期一个月' % (keyword_rank.text))
        if create_action(request.user, '续期了', keyword_rank):
            user_setting=UserSettings.objects.filter(user=request.user)
            user_setting.update(credit=F('credit')-6)
        return redirect('/keyword_rank/')
    else:
        messages.success(request, '%s的监控时间超过三个月,请不要继续续期' % (keyword_rank.text))
        return redirect('/keyword_rank/')


def delete(request, id):
    keyword_rank=get_object_or_404(Keyword_rank, id=id)
    if Rank_to_user.objects.filter(keyword_rank=keyword_rank,user=request.user):
        Rank_to_user.objects.filter(keyword_rank=keyword_rank,user=request.user).delete()
        messages.success(request, '已经删除%s' % (keyword_rank.text))
        return redirect('/keyword_rank/')

"""
@login_required
def rank_detail(request, slug):
    keyword_rank = get_object_or_404(Keyword_rank, slug = slug)

    form = Keyword_rank_Form(data=request.POST or None)
    if form.is_valid():
        new_asin = form.save(commit=False)
        if not Keyword_rank.objects.filter(asin=new_asin.asin,country=new_asin.country,word=new_asin.word):
            amazon = amazon_api(new_asin.country)
            new_asin.title = find_item(amazon,new_asin.asin)
            new_asin.save()
        keyword_rank = Keyword_rank.objects.filter(asin=new_asin.asin,word=new_asin.word,country=new_asin.country)[0]
        print(keyword_rank)

        user_setting= UserSettings.objects.filter(user=request.user)
        if user_setting[0].credit < 4:
            return redirect('/recharge')

        task = rank_in_web.delay(keyword_rank.asin,keyword_rank.word,keyword_rank.country)
        while AsyncResult(task.task_id).status != 'SUCCESS':
            if AsyncResult(task.task_id).status == 'FAILURE':
                messages.error(request, '发生网络错误,请稍后再次查询.本次查询没有扣除积分.')
                return redirect('/keyword_rank')
            pass
        if AsyncResult(task.task_id).status == 'SUCCESS':
            rank_to_user=Rank_to_user(keyword_rank=keyword_rank,user=request.user,expired=timezone.now() + datetime.timedelta(days=30))
            rank_to_user.save()
            if create_action(request.user, '查询了', keyword_rank):
                user_setting.update(credit=F('credit')-4)
    ranks = Rank.objects.filter(keyword_rank=keyword_rank)
    return render(request, 'crawler/keyword_rank/rank_detail.html', {'form':form, 'keyword_rank': keyword_rank, 'ranks':ranks})


if form.is_valid():
    new_asin = form.save(commit=False)
    if not Keyword_rank.objects.filter(asin=new_asin.asin,country=new_asin.country):
        amazon = amazon_api(new_asin.country)
        new_asin.title = find_item(amazon,new_asin.asin)
        new_asin.save()
    keyword_rank = Keyword_rank.objects.filter(asin=new_asin.asin,country=new_asin.country)[0]
    print(keyword_rank)

rank_form = Rank_Form(data=request.POST or None)
if rank_form.is_valid():
    user_setting= UserSettings.objects.filter(user=request.user)
    if user_setting[0].credit < 4:
        return redirect('recharge')
    new_word = rank_form.save(commit=False)
    if Rank.objects.filter(keyword_rank=keyword_rank,word=new_word.word):
        rank = Rank.objects.filter(keyword_rank=keyword_rank,word=new_word.word)[0]
        if not Rank_to_user.objects.filter(rank=rank,user=request.user,expired__gte=timezone.now()):
            rank_to_user=Rank_to_user(keyword_rank=keyword_rank,rank=rank,user=request.user,expired=timezone.now() + datetime.timedelta(days=30))
            rank_to_user.save()
            if create_action(request.user, '查询了', rank):
                user_setting.update(credit=F('credit')-4)
            return redirect(keyword_rank.get_absolute_url())
    else:
        task = rank_in_web.delay(keyword_rank.asin,new_word.word,keyword_rank.country)
        while AsyncResult(task.task_id).status != 'SUCCESS':
            pass
        if AsyncResult(task.task_id).status == 'SUCCESS':
            rank = Rank.objects.filter(keyword_rank=keyword_rank,word=new_word.word)[0]
            rank_to_user=Rank_to_user(keyword_rank=keyword_rank,rank=rank,user=request.user,expired=timezone.now() + datetime.timedelta(days=30))
            rank_to_user.save()
            if create_action(request.user, '查询了', rank):
                user_setting.update(credit=F('credit')-4)

    rank_to_users = Rank_to_user.objects.filter(user=request.user,keyword_rank=keyword_rank)
    ranks = rank_to_users.values_list('rank', flat=True)
    ranks = Rank.objects.filter(id__in=ranks)
"""