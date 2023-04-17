from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views import generic
from datetime import datetime

from process_manager.models import Phase, Activity, Project,Task
from dashboard.tasks.forms import TaskForm, UpdateTaskForm
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
    
def delete(request, id):
  task = Task.objects.get(id=id)
  
  if request.method == 'POST':
      nsc = NoSQLClient()
      nsc_database = nsc.get_db("process_design")
      new_document = nsc_database.get_query_result(
            {"_id": task.couch_id}
           )[0]
      if new_document:
          nsc.delete_document(nsc_database,task.couch_id)
          task.delete()

          return redirect('dashboard:tasks:list')
      
  return render(request,'tasks/task_confirm_delete.html',
                    {'task': task})


class UpdateTaskView(PageMixin, LoginRequiredMixin, AdminPermissionRequiredMixin, generic.UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    title = gettext_lazy('Edit Task')
    active_level1 = 'tasks'
    form_class = UpdateTaskForm
    # success_url = reverse_lazy('dashboard:projects:list')
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
    
    task_db = None
    task = None
    doc = None
    task_db_name = None

    def dispatch(self, request, *args, **kwargs):
        nsc = NoSQLClient()
        try:
            self.task = self.get_object()
            self.task_db_name = 'process_design'
            self.task_db = nsc.get_db(self.task_db_name)
            query_result = self.task_db.get_query_result({"type": "task"})[:]
            self.doc = self.task_db[query_result[0]['_id']]
        except Exception:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(UpdateTaskView, self).get_context_data(**kwargs)
        form = ctx.get('form')
        ctx.setdefault('task_doc', self.doc)
        if self.doc:
            if form:
                for label, field in form.fields.items():
                    try:
                        form.fields[label].value = self.doc[label]
                    except Exception as exc:
                        pass
                    
                ctx.setdefault('form', form)

        return ctx

    def post(self, request, *args, **kwargs):
        
        if not self.task_db_name:
            raise Http404("We don't find the database name for the Task.")

        form = UpdateTaskForm(request.POST, instance=self.task)
        if form.is_valid():
            return self.form_valid(form)
        return self.get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        task = form.save(commit=False)
        task.name=data['name'] 
        task.description=data['description']
        task.activity = data['activity']       
        task.phase = task.activity.phase
        task.project = task.activity.phase.project
        task.form = data['form']
        task.order = data['order']       
        task.save()         
        doc = {
            "type": "task",
            "project_id": task.activity.phase.project.couch_id,
            "phase_id": task.activity.phase.couch_id,
            "phase_name": task.activity.phase.name,
            "activity_id": task.activity.couch_id,
            "activity_name": task.activity.name,
            "name": data['name'],
            "order": data['order'],
            "description": data['description'],
            "completed": False,
            "completed_date": "",
            "capacity_attachments": [],
            "attachments": [],
            "form": data['form'],
            "form_response": [],
            "sql_id": task.id
        }
        nsc = NoSQLClient()
        query_result = self.task_db.get_query_result({"_id": task.couch_id})[:]
        self.doc = self.task_db[query_result[0]['_id']]
        nsc.update_doc(self.task_db, self.doc['_id'], doc)
        return redirect('dashboard:tasks:list')
