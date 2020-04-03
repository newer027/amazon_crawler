#-*- coding:utf-8 -*-

from django.views.generic import TemplateView
from . import views
from django.conf.urls import url


urlpatterns =[
    url(r'^$', TemplateView.as_view(template_name="crawler/payment/recharge.html"), name='recharge'),
    url(r'^success/$', TemplateView.as_view(template_name="crawler/payment/success.html"), name="payment_success"),
    url(r'^error/$', TemplateView.as_view(template_name="crawler/payment/error.html"), name="payment_error"),
    url(r'^upgrade/(?P<add_credit>\w+)/$', views.upgrade_account, name="upgrade_account"),
    url(r'^return_url/$', views.return_url_handler, name="payment_return_url"),
    url(r'^notify_url/$', views.notify_url_handler, name="payment_notify_url"),
]