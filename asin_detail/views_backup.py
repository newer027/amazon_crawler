from django.shortcuts import render, redirect, get_object_or_404
from .forms import Asin_detail_Form
from .models import Asin_detail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import generics
from asin_detail.serializers import Asin_Detail_Serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@login_required
def asin_submit(request):
    asin_details = Asin_detail.objects.filter(user=request.user)
    asin_details = asin_details.order_by('-created')
    form = Asin_detail_Form(data=request.POST or None)
    """
    if form.is_valid():
        new_asin = form.save(commit=False)
        for asin in new_asin.asins_in.splitlines():
            if not Asin_detail.objects.filter(asin=asin,country=new_asin.country,user=User.objects.get(id=request.user.id)):
                asin_detail=Asin_detail(asin=asin,country=new_asin.country,user=User.objects.get(id=request.user.id))
                asin_detail.save()
        messages.success(request, '查询任务已经保存,稍后开始为您查询.')
        return redirect('/asin_detail/')
    """
    return render(request, 'crawler/asin_detail/asin_submit.html', {'form': form,'asin_details': asin_details,})


"""
def delete(request, id):
    get_object_or_404(Asin_detail, id=id).delete()
    return redirect('/asin_detail')
"""


class Asin_Detail_Delete(generics.RetrieveDestroyAPIView):
    queryset = Asin_detail.objects.all()
    serializer_class = Asin_Detail_Serializer



@api_view(['GET', 'POST'])
def post_collection(request):
    if request.method == 'GET':
        posts = Asin_detail.objects.all()
        serializer = Asin_Detail_Serializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {'text': request.DATA.get('the_post'), 'user': request.user}
        serializer = Asin_Detail_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)