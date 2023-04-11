from django.urls import path

from dashboard.activities import views

app_name = 'activities'
urlpatterns = [
    path('', views.ActivityListView.as_view(), name='list'),
    path('activities-list/', views.ActivityListTableView.as_view(), name='activities_list'),
]
