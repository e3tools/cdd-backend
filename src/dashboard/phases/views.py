from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views import generic
from datetime import datetime

from process_manager.models import Phase, Project
from dashboard.phases.forms import PhaseForm, UpdatePhaseForm
from dashboard.mixins import AJAXRequestMixin, PageMixin, JSONResponseMixin
from no_sql_client import NoSQLClient

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

class CreatePhaseFormView(PageMixin, LoginRequiredMixin, AdminPermissionRequiredMixin, generic.FormView):
    template_name = 'phases/create.html'
    title = gettext_lazy('Create Phase')
    active_level1 = 'phases'
    form_class = PhaseForm
    success_url = reverse_lazy('dashboard:phases:list')
    breadcrumb = [
        {
            'url': reverse_lazy('dashboard:phases:list'),
            'title': gettext_lazy('Phases')
        },
        {
            'url': '',
            'title': title
        }
    ]

    def form_valid(self, form):
        data = form.cleaned_data
        project = Project.objects.get(id=data['project'])
        phase = Phase(
            name=data['name'], 
            description=data['description'],
            project = project,
            order = data['order'])
        phase.save()        
        return super().form_valid(form)
    
class UpdatePhaseView(PageMixin, LoginRequiredMixin,AdminPermissionRequiredMixin, generic.UpdateView):
    model = Phase
    template_name = 'phases/update.html'
    title = gettext_lazy('Edit Phase')
    active_level1 = 'phases'
    form_class = UpdatePhaseForm
    # success_url = reverse_lazy('dashboard:projects:list')
    breadcrumb = [
        {
            'url': reverse_lazy('dashboard:phases:list'),
            'title': gettext_lazy('Phases')
        },
        {
            'url': '',
            'title': title
        }
    ]
    
    phase_db = None
    phase = None
    doc = None
    phase_db_name = None

    def dispatch(self, request, *args, **kwargs):
        nsc = NoSQLClient()
        try:
            self.phase = self.get_object()
            self.phase_db_name = 'process_design'
            self.phase_db = nsc.get_db(self.phase_db_name)
            query_result = self.phase_db.get_query_result({"type": "phase"})[:]
            self.doc = self.phase_db[query_result[0]['_id']]
        except Exception:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(UpdatePhaseView, self).get_context_data(**kwargs)
        form = ctx.get('form')
        ctx.setdefault('phase_doc', self.doc)
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
        
        if not self.phase_db_name:
            raise Http404("We don't find the database name for the phase.")

        form = UpdatePhaseForm(request.POST, instance=self.phase)
        if form.is_valid():
            return self.form_valid(form)
        return self.get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        project = Project.objects.get(id=data['project'])
        phase = form.save(commit=False)
        phase = Phase(
            name=data['name'], 
            description=data['description'],
            couch_id = data['couch_id'],
            project = project,
            order = data['order'])
        phase.save()          
        doc = {          
            "name": data['name'],
            "type": "phase",
            "description": data['description'],
            "order":data['order'],
            "capacity_attachments": [],
            "sql_id": phase.id
        }
        nsc = NoSQLClient()
        query_result = self.phase_db.get_query_result({"type": "phase","_id": phase.couch_id})[:]
        self.doc = self.phase_db[query_result[0]['_id']]
        nsc.update_doc(self.phase_db, self.doc['_id'], doc)
        return redirect('dashboard:phase:list')
    
