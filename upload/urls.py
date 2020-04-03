from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.FileListView.as_view(), name='file_list'),
    url(r'^(?P<pk>\d+)/$', views.FileDetailView, name='file_detail'),
    url(r'^(?P<pk>\d+)/delete/$', views.FileDeleteView.as_view(), name='file_delete'),
    url(r'^create/$', views.FileCreateView.as_view(), name='file_create'),
]


