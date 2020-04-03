from django.contrib import admin
from .tasks import import_user
from .models import ImportFile, Asin_detail


class ImportFileAdmin(admin.ModelAdmin):

    list_display = ('file','name',)

    def save_model(self, request, obj, form, change):

        re = super(ImportFileAdmin,self).save_model(request, obj, form, change)
        import_user.delay(obj.file.path)
        return re


admin.site.register(ImportFile, ImportFileAdmin)


class Asin_detail_Admin(admin.ModelAdmin):
    list_display = ['country', 'asin', 'title', 'created']
    search_fields = ['country', 'asin', 'fu_asin', 'title','asin']

admin.site.register(Asin_detail, Asin_detail_Admin)

