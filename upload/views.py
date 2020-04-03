from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from .models import Document
from django.shortcuts import redirect
from django.contrib.staticfiles.templatetags.staticfiles import static


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset() #super, get_queryset的用法
        return qs.filter(owner=self.request.user) #filter的用法


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user #.instance.owner的用法
        return super(OwnerEditMixin, self).form_valid(form) #form_valid的用法


class OwnerFileMixin(OwnerMixin, LoginRequiredMixin): #OwnerMixin的用法
    model = Document


class OwnerFileEditMixin(OwnerFileMixin, OwnerEditMixin): #OwnerEditMixin的用法
    fields = ['description', 'document']
    success_url = reverse_lazy('upload:file_list') #reverse_lazy的用法
    template_name = 'crawler/upload/form.html' #template_name的用法


class FileListView(OwnerFileMixin, ListView):
    template_name = 'crawler/upload/list.html'


class FileCreateView(PermissionRequiredMixin,
                       OwnerFileEditMixin,
                       CreateView):
    permission_required = 'upload.add_document'


class FileDeleteView(PermissionRequiredMixin,
                       OwnerFileMixin,
                       DeleteView):
    success_url = reverse_lazy('upload:file_list')
    template_name = 'crawler/upload/delete.html'
    permission_required = 'upload.delete_document'


def FileDetailView(request,pk):
    file = Document.objects.filter(pk=pk)[0]
    return redirect(static(file.document.name[6:]))