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

class TaskListView(PageMixin, LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.all()
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    title = gettext_lazy('Tasks')
    active_level1 = 'tasks'
    breadcrumb = [
        {
            'url': '',
            'title': title
        },
    ]

    def get_queryset(self):
        return super().get_queryset()
    

class TaskListTableView(LoginRequiredMixin, generic.ListView):
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_results(self):
        tasks = []        
        tasks = list(Task.objects.all())
        return tasks

    def get_queryset(self):

        return self.get_results()
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


    
