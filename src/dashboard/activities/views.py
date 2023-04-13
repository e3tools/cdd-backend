from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views import generic
from datetime import datetime

from process_manager.models import Phase, Activity, Project
from dashboard.activities.forms import ActivityForm
from dashboard.mixins import AJAXRequestMixin, PageMixin, JSONResponseMixin
from no_sql_client import NoSQLClient

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
class CreateActivityFormView(PageMixin, LoginRequiredMixin, AdminPermissionRequiredMixin, generic.FormView):
    template_name = 'activities/create.html'
    title = gettext_lazy('Create Activity')
    active_level1 = 'activities'
    form_class = ActivityForm
    success_url = reverse_lazy('dashboard:activities:list')
    breadcrumb = [
        {
            'url': reverse_lazy('dashboard:activities:list'),
            'title': gettext_lazy('Phases')
        },
        {
            'url': '',
            'title': title
        }
    ]

    def form_valid(self, form):
        data = form.cleaned_data
        #project = Project.objects.get(id = data['project'])
        phase = Phase.objects.get(id = data['phase'])
        activity = Activity(
            name=data['name'], 
            description=data['description'],
            project = phase.project,
            phase = phase,
            total_tasks = data['total_tasks'],
            order = data['order'])
        activity.save()        
        return super().form_valid(form)

    
