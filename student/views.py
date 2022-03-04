from pyexpat import model
from django.conf import settings
from django.shortcuts import render
from student.models import Student
from quiz import models as QMODEL
from django.contrib.auth.decorators import login_required,user_passes_test
from quiz.models import Result, Course
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls.base import reverse_lazy
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.mixins import LoginRequiredMixin

# pdf settings imports
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


# Create your views here.

class StudentListView(ListView, LoginRequiredMixin):
    model = Student
    template_name = 'student/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = 'testing'
        context['student'] = Student.objects.all()
        context['students'] = Student.objects.get(user=self.request.user)
        return context 


# admin result view

class Admin_result(LoginRequiredMixin, ListView):
    models = QMODEL.Course
    template_name = 'student/admin_result.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return QMODEL.Course.objects.all()

    def get_context_data(self, **kwargs):

        context= super().get_context_data(**kwargs)
        context['course_count'] =QMODEL.Course.objects.all().count()
        context['question_count'] =QMODEL.Question.objects.all().count()
        context['result_count'] =QMODEL.Result.objects.all().count()
        context['student_count'] = Student.objects.all().count()
        return context


  
@login_required
def Admin_detail_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = Student.objects.get(user_id=request.user.id)

    # m = QMODEL.Result.objects.aggregate(Max('marks'))   
    # max_q = QMODEL.Result.objects.filter(student_id = OuterRef('student_id'), exam_id = OuterRef('exam_id') ,).order_by('-marks').values('id')
    max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    results = Result.objects.filter(id = Subquery(max_q[:1]), exam=course).order_by('-marks')
    Result.objects.filter(id__in = Subquery(max_q[1:]), exam=course, marks = 1).delete()   
    # max_q = QMODEL.Result.objects.filter(marks = OuterRef('marks') ,).order_by('-marks').values('id')
    # results = QMODEL.Result.objects.filter(id = Subquery(max_q[:1]), marks__gte =2)
    # QMODEL.Result.objects.exclude(id = results[:1]).delete() 
    # QMODEL.Result.objects.get(~Q(id = results[:1]), student_id = results[:1].student.id, exam_id = results[:1].exam.id).delete()

    
    context = { 
        'results':results,
        'course':course,
        'st':request.user,
     
    }
    return render(request,'student/Admin_result_detail_view.html', context)

# student result sections

class Student_result(LoginRequiredMixin, ListView):
    models = QMODEL.Course
    template_name = 'student/student_result.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return QMODEL.Course.objects.all()

@login_required
def userprofileview(request,pk):
    # course=QMODEL.Course.objects.get(id=pk)
    # student = Profile.objects.get(user_id=request.user.id)
    # student = request.user.id  
    # m = QMODEL.Result.objects.aggregate(Max('marks'))  
    # max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    # results = Result.objects.filter(id = Subquery(max_q[:1]), exam=course, student = student)
    # Result.objects.filter(id__in = Subquery(max_q[1:]), exam=course)
      
    
    # QMODEL.Result.objects.exclude(id = m).delete()
    # user_profile =  Student.objects.filter(user_id = request.user)
    
    course=QMODEL.Course.objects.get(id=pk)
    student = Student.objects.get(user_id=request.user.id)
    results=QMODEL.Result.objects.all().filter(exam=course,student=student).order_by('-marks')
              
    context = {
        'results':results,
        'course':course,  
    }
    return render(request,'student/profile.html', context)

class Topscoreslistview(LoginRequiredMixin, ListView):
    models = QMODEL.Course
    template_name = 'student/topscorelistview.html'
    count_hit = True
   
    def get_queryset(self):
        return QMODEL.Course.objects.all()
    
    def get_context_data(self, **kwargs):

        context= super().get_context_data(**kwargs)
        context['course_count'] =QMODEL.Course.objects.all().count()
        context['question_count'] =QMODEL.Question.objects.all().count()
        context['result_count'] =QMODEL.Result.objects.all().count()
        context['student_count'] = Student.objects.all().count()
        return context

def Topscores_pdf_view(request, pk):

    course=QMODEL.Course.objects.get(id=pk)
    student = Student.objects.get(user_id=request.user.id)

    # m = QMODEL.Result.objects.aggregate(Max('marks'))   
    # max_q = QMODEL.Result.objects.filter(student_id = OuterRef('student_id'), exam_id = OuterRef('exam_id') ,).order_by('-marks').values('id')
    max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    results = Result.objects.filter(id = Subquery(max_q[:1]), exam=course).order_by('-marks')
    Result.objects.filter(id__in = Subquery(max_q[1:]), exam=course, marks = 1).delete()   
    # max_q = QMODEL.Result.objects.filter(marks = OuterRef('marks') ,).order_by('-marks').values('id')
    # results = QMODEL.Result.objects.filter(id = Subquery(max_q[:1]), marks__gte =2)
    # QMODEL.Result.objects.exclude(id = results[:1]).delete() 
    # QMODEL.Result.objects.get(~Q(id = results[:1]), student_id = results[:1].student.id, exam_id = results[:1].exam.id).delete()

    
    context = { 
        'results':results,
        'course':course,
        'st':request.user,
     
    }

    template_path = 'student/topscoresdetailviewpdf.html'
    # context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response