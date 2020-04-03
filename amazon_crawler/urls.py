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
from django.conf.urls import url, include
from django.contrib import admin
from . import views
import debug_toolbar
from django.contrib.auth.views import (
    password_reset_done,
    password_reset_confirm,
    password_reset_complete)


urlpatterns = [
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^guwei_administration/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^find_none/', views.find_none, name='find_none'),
    url(r'^converter/', views.converter, name='converter'),
    url(r'^keyword_rank/', include('keyword_rank.urls', namespace='keyword_rank')),
    url(r'^rele_keyword/', include('rele_keyword.urls', namespace='rele_keyword')),
    url(r'^inventory/', include('inventory.urls', namespace='inventory')),
    url(r'^asin_keyword/', include('asin_keyword.urls', namespace='asin_keyword')),
    url(r'^asin_detail/', include('asin_detail.urls', namespace='asin_detail')),
    url(r'^follow_sale/', include('follow_sale.urls', namespace='follow_sale')),
    url(r'^prime_asins/', include('prime_asins.urls', namespace='prime_asins')),
    url(r'^review_monitor/', include('review_monitor.urls', namespace='review_monitor')),
    url(r'^review_qa_collect/', include('review_qa_collect.urls', namespace='review_qa_collect')),
    url(r'^short_url/', include('short_url.urls', namespace='short_url')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^actions/', include('actions.urls', namespace='actions')),
    url(r'^upload/', include('upload.urls', namespace='upload')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^recharge/', include('payment.urls', namespace='payment')),
    url(r'^upload/', include('upload.urls', namespace='upload')),
    url(r'^core/', include('core.urls', namespace='core')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^(?P<shorten_id>\w{6})$',views.redirect_original, name='redirectoriginal'),
    url(r'^password/reset/done/$',password_reset_done,name='password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',password_reset_confirm,name='password_reset_confirm'),
    url(r'^password_reset_complete/$',password_reset_complete,name='password_reset_complete'),
    url(r'^check/', views.check, name='check'),
    # when short URL is requested it redirects to original URL
]
