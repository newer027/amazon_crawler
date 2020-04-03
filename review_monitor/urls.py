"""amazon_crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.product_submit, name='product_submit'),
    url(r'^(?P<slug>[\w-]+)/$',views.product_detail,name='product_detail'),
    url(r'^more_monitor/(?P<id>\d+)/$', views.more_monitor, name="more_monitor"),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name="delete"),
]
