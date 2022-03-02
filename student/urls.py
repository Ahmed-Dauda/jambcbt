
from django.urls import path
from student.views import (
    StudentListView,
    Admin_result,
    Student_result,
    Topscoreslistview
    )
from . import views

app_name = 'student'

urlpatterns = [
   
    path('student-details', StudentListView.as_view(), name = 'student-details'),
    path('admin_result', Admin_result.as_view(), name ='admin_result'),
    path('student_result', Student_result.as_view(), name ='student_result'),
    path('userprofileview/<pk>/', views.userprofileview, name ='userprofileview'),
    path('topscoreslistview', Topscoreslistview.as_view(), name ='topscoreslistview'),
    path('topscores_pdf_view/<pk>/', views.Topscores_pdf_view, name ='topscores_pdf_view'),
    path('admin_result_detail_view/<pk>/', views.Admin_detail_view, name ='admin_result_detail_view'),
]
