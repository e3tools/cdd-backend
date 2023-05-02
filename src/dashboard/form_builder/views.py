from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy
from django.shortcuts import redirect, get_list_or_404
from dashboard.mixins import AJAXRequestMixin, PageMixin, JSONResponseMixin
from no_sql_client import NoSQLClient
from process_manager.models import FormType
from form_builder.forms import FormTypeForm

from authentication.permissions import (
    CDDSpecialistPermissionRequiredMixin, SuperAdminPermissionRequiredMixin,
    AdminPermissionRequiredMixin
    )

class FormTypeListView(PageMixin, LoginRequiredMixin, generic.ListView):
    model = FormType
    queryset = FormType.objects.all()
    template_name = 'form_builder/form_type/list.html'
    context_object_name = 'form_types'
    title = gettext_lazy('Form Types')
    breadcrumb = [{
            'url': '',
            'title': title
        }]
    
    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FormTypeForm()
        return context

class CreateFormTypeView(PageMixin, LoginRequiredMixin, AdminPermissionRequiredMixin, generic.FormView):
    template_name = 'form_builder/form_type/list.html'
    title = gettext_lazy("Create Form Type")
    active_level1 = "form_types"
    form_class = FormTypeForm
    success_url = reverse_lazy('dashboard:form_builder:form_type_list')
    breadcrumb = [{
        'url': reverse_lazy('dashboard:form_builder:form_type_list'),
        'title': gettext_lazy('Form Types')
    },
    {
        'url': '',
        'title': title
    }]


# class FormTypeMixin:
#     doc = None
#     obj = None
#     db = None
#     db_name = None
#     content_type = None #Type of data that we should pull

#     def dispatch(self, *args, **kwargs):
#         nsc = NoSQLClient()
#         try:
#             self.db_name = kwargs["id"]
#             self.content_type = kwargs["ctype"]
#             self.db = nsc.get_db(self.db_name)
#             query_result = self.db.get_query_result({"type": self.content_type})
#         except Exception:
#             raise Http404