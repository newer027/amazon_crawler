from django.contrib.auth.models import User
from rest_framework import serializers
from asin_detail.models import Asin_detail


class Asin_Detail_Serializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        queryset=User.objects.filter(), slug_field='username'
    )

    class Meta:
        model = Asin_detail
        fields = ('id', 'asin', 'title', 'country', 'img_url','detail_page_url','price','brand','label','bsr_rank','user','created')
