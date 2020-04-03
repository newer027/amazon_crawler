from django.contrib import admin
from .models import QA_detail, Review_detail


@admin.register(QA_detail)
class QA_Admin(admin.ModelAdmin):
    list_display = ['product', 'question','answer', 'answer_url',]
    search_fields = ['product__asin',]


@admin.register(Review_detail)
class Review_Admin(admin.ModelAdmin):
    list_display = ['product', 'star','customer_id', 'review_text','normal']
    search_fields = ['product__asin',]