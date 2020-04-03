from django.conf.urls import url
from .views import action


urlpatterns = [
    url(r'^$',action,name='action'),
]