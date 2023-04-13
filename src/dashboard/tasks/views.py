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
from dashboard.tasks.forms import TaskForm
from dashboard.mixins import AJAXRequestMixin, PageMixin, JSONResponseMixin
from no_sql_client import NoSQLClient

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

class CreateTaskFormView(PageMixin, LoginRequiredMixin, AdminPermissionRequiredMixin, generic.FormView):
    template_name = 'tasks/create.html'
    title = gettext_lazy('Create Task')
    active_level1 = 'tasks'
    form_class = TaskForm
    success_url = reverse_lazy('dashboard:tasks:list')
    breadcrumb = [
        {
            'url': reverse_lazy('dashboard:tasks:list'),
            'title': gettext_lazy('Tasks')
        },
        {
            'url': '',
            'title': title
        }
    ]

    def form_valid(self, form):
        data = form.cleaned_data
        #project = Project.objects.get(id = data['project'])
        #phase = Phase.objects.get(id = data['phase'])
        activity = Activity.objects.get(id = data['activity'])
        form = [] 
        if data['form']:
            form = data['form']
        task = Task(
            name=data['name'], 
            description=data['description'],
            project = activity.phase.project,
            phase = activity.phase,
            activity = activity,
            order = data['order'],
            form = form
            )
        task.save()        
        return super().form_valid(form)
    
