from django.urls import path

from dashboard.form_builder import views
#from dashboard.activities import views as activityView

app_name = 'form_builder'
urlpatterns = [
    path('', views.FormTypeListView.as_view(), name='form-type-list'),
    path('form-type-list/', views.FormTypeListView.as_view(), name='form-type-list'),
    path('create-form-type/', views.CreateFormTypeView.as_view(), name='create-form-type'),    
    path('create-form-type/<int:id>', views.CreateFormTypeView.as_view(), name='create-form-type'),
    path('<int:pk>/update-form-type/', views.UpdateFormTypeView.as_view(), name='update'),
    # path('delete/<int:id>', views.delete, name='delete'),
    # path('MoveUp/<int:id>', views.changeOrderUp, name='MoveUp'),
    # path('MoveDown/<int:id>', views.changeOrderDown, name='MoveDown'),
    # path('Detail/<int:id>', views.task_detail_view, name='task_Detail'),
    # path('Detail/<int:id>', activityView.activity_detail_view, name='activity_Detail'),
]
