
from django.urls import path
from . import views
from quiz.views import (
    DashboardListView, 
    ProfileListView,
    StudentEnrollment,
    InstructionListView
)
app_name = 'quiz'

urlpatterns = [
   
    path('', views.index, name = 'index'),
    # path('base', views.table, name = 'base'),
    path('home', views.home, name = 'home'),
    path('studentenrollment', StudentEnrollment.as_view(), name = 'studentenrollment'),
    path('dashboardlistview', DashboardListView.as_view(), name = 'dashboardlistview'),
    path('profilelistview', ProfileListView.as_view(), name = 'profilelistview'),
    path('instructionlistview', InstructionListView.as_view(), name = 'instructionlistview'),
    

    path('take-exam', views.take_exams_view,name='take-exam'),
    path('start-exam/<pk>/', views.start_exams_view,name='start-exam'),
    path('calculate_marks', views.calculate_marks_view,name='calculate_marks'),
    path('view_result', views.view_result_view,name='view_result'),
    path('check_marks/<pk>/', views.check_marks_view,name='check_marks'),
    # path('myview', views.myview, name = 'myview'),
    # path('add', views.add_students, name = 'add'),
    # path('update/<pk>/', views.update_students, name = 'update'),
    # path('delete/<pk>/', views.delete_students, name = 'delete'),
    # path('pdf_all', views.pdf_all_view, name = 'pdf_all'),
    # path('pdf_id/<int:pk>/', views.pdf_id_view, name = 'pdf_id'),
]
