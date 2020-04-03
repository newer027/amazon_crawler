# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest


def ajax_required(f):
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest() #不存在request.is_ajax()
            return f(request, *args, **kwargs) #存在request.is_ajax()
    wrap.__doc__=f.__doc__ #__doc__的用法
    wrap.__name__=f.__name__ #__name__的用法
    return wrap