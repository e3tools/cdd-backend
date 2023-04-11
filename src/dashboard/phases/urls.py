from django.urls import path

from dashboard.phases import views

app_name = 'phases'
urlpatterns = [
    path('', views.PhaseListView.as_view(), name='list'),
    path('phases-list/', views.PhaseListTableView.as_view(), name='phases_list'),
]
