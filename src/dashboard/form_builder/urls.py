from django.urls import path

from dashboard.form_builder import views
#from dashboard.activities import views as activityView

app_name = 'form_builder'
urlpatterns = [
    path('', views.FormTypeListView.as_view(), name='list_form_type'),
    path('form-types/', views.FormTypeListView.as_view(), name='list_form_type'),
    path('create-form-type/', views.CreateFormTypeView.as_view(), name='create_form_type'),    
    path('update-form-type/<int:pk>', views.CreateFormTypeView.as_view(), name='update_form_type'),    
    path('delete-form-type/<int:pk>', views.UpdateFormTypeView.as_view(), name='delete_form_type'),
    path('form-fields/<int:id>', views.CreateFormTypeView.as_view(), name='list_form_fields'),
    # path('delete/<int:id>', views.delete, name='delete'),
    # path('MoveUp/<int:id>', views.changeOrderUp, name='MoveUp'),
    # path('MoveDown/<int:id>', views.changeOrderDown, name='MoveDown'),
    # path('Detail/<int:id>', views.task_detail_view, name='task_detail'),
    # path('Detail/<int:id>', activityView.activity_detail_view, name='activity_Detail'),
]
