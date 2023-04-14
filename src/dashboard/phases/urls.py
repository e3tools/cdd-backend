from django.urls import path

from dashboard.phases import views

app_name = 'phases'
urlpatterns = [
    path('', views.PhaseListView.as_view(), name='list'),
    path('phases-list/', views.PhaseListTableView.as_view(), name='phases_list'),
    path('create/', views.CreatePhaseFormView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdatePhaseView.as_view(), name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
]
