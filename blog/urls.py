from django.conf.urls import url

from .views import BlogDetailView, BlogListView, BlogTagListView


urlpatterns = [
    url(r'^$',BlogListView.as_view(),name='blog_list_view'),
    url(r'^tag/(?P<tag>[\w ]+)/$',BlogTagListView.as_view(),name='blog_tag_list_view'),
    url(r'^(?P<slug>[\w-]+)/$',BlogDetailView.as_view(),name='blog_detail_view'),
]
