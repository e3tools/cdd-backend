from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views import generic
from datetime import datetime

from process_manager.models import Phase, Activity, Project,Task
from authentication.models import Facilitator
from dashboard.facilitators.forms import FacilitatorForm, FilterTaskForm, UpdateFacilitatorForm, FilterFacilitatorForm
from dashboard.mixins import AJAXRequestMixin, PageMixin, JSONResponseMixin
from no_sql_client import NoSQLClient
from dashboard.utils import (
    get_all_docs_administrative_levels_by_type_and_administrative_id,
    get_all_docs_administrative_levels_by_type_and_parent_id
)
from authentication.permissions import (
    CDDSpecialistPermissionRequiredMixin, SuperAdminPermissionRequiredMixin,
    AdminPermissionRequiredMixin
    )

class PhaseListView(PageMixin, LoginRequiredMixin, generic.ListView):
    model = Phase
    queryset = Phase.objects.all()
    template_name = 'phases/list.html'
    context_object_name = 'phases'
    title = gettext_lazy('Phases')
    active_level1 = 'phases'
    breadcrumb = [
        {
            'url': '',
            'title': title
        },
    ]

    def get_queryset(self):
        return super().get_queryset()
    

class PhaseListTableView(LoginRequiredMixin, generic.ListView):
    template_name = 'phases/phase_list.html'
    context_object_name = 'phases'

    def get_results(self):
        phases = []        
        phases = list(Phase.objects.all())
        return phases

    def get_queryset(self):

        return self.get_results()
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


    
