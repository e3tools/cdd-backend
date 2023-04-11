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

class ActivityListView(PageMixin, LoginRequiredMixin, generic.ListView):
    model = Activity
    queryset = Activity.objects.all()
    template_name = 'activities/list.html'
    context_object_name = 'activities'
    title = gettext_lazy('Activities')
    active_level1 = 'activities'
    breadcrumb = [
        {
            'url': '',
            'title': title
        },
    ]

    def get_queryset(self):
        return super().get_queryset()
    

class ActivityListTableView(LoginRequiredMixin, generic.ListView):
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'

    def get_results(self):
        activities = []        
        activities = list(Activity.objects.all())
        return activities

    def get_queryset(self):

        return self.get_results()
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


    
