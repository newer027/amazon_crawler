from django.shortcuts import render
from .forms import In_word_Form
from .rele_keyword import get_rele_word
from celery import group
import itertools


def in_word(request):
    out_words=None
    form = In_word_Form(data=request.POST or None)
    if form.is_valid():
        new_word=form.save(commit=False)
        second_word=get_rele_word.s(new_word.in_word,new_word.country)
        third_words=group(get_rele_word.s(i,new_word.country) for i in second_word())()
        out_words = []
        for i in third_words:
            try:
                out_words+=i.get()
            except:
                pass
    return render(request, 'crawler/rele_keyword/in_word.html', {'form':form, 'out_words': out_words})