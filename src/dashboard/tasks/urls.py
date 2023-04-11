from django.urls import path

from dashboard.tasks import views

app_name = 'tasks'
urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('tasks-list/', views.TaskListTableView.as_view(), name='tasks_list'),
]
