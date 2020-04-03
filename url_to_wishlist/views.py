from django.shortcuts import render
from .forms import Url_to_wishlist_Form
from .models import Url_to_wishlist


def url_list(request):
    urls = Url_to_wishlist.objects.all()
    form = Url_to_wishlist_Form(data=request.POST or None)
    if form.is_valid():
        new_url = form.save(commit=False)
        new_url.save()
    return render(request, 'crawler/url_to_wishlist/url_list.html', {'form': form,'urls': urls})