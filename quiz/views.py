from multiprocessing import context
from django import views
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from student.models import Student
from quiz import models as QMODEL
from quiz.models import Result, Course
from django.urls.base import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models import Max, Subquery, OuterRef
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'quiz/index.html')

class StudentEnrollment(ListView, LoginRequiredMixin):
    
    template_name = 'quiz/dashboard/tables.html'
    def get_queryset(self):
        return Student.objects.all()

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        context['course_count'] =QMODEL.Course.objects.all().count()
        context['question_count'] =QMODEL.Question.objects.all().count()
        context['result_count'] =QMODEL.Result.objects.all().count()
        context['student_count'] = Student.objects.all().count()
        context['student'] = Student.objects.get(user_id=self.request.user.id)
        return context

    # student_sta = Student.objects.all()
    # student = Student.objects.get(user_id=request.user.id)
    # context = {
    #     'student_sta':student_sta,
    #     'student':student
    # }
    # return render(request, 'quiz/dashboard/tables.html',context)

def home(request):
    return render(request, 'quiz/home.html')


class DashboardListView(ListView, LoginRequiredMixin):
    model = Course
    template_name = 'quiz/dashboard/dashboard.html'
    
    def get_queryset(self):
        return Course.objects.all()

# def ProfileListView(request, pk):
#     course_count =QMODEL.Course.objects.get(id=pk).count()
#     student_count = Student.objects.all().count()

#     context ={
#         'course_count':course_count,
#         'student_count':student_count
#     }
#     return render(request, 'quiz/dashboard/profile.html', context)

class ProfileListView(ListView, LoginRequiredMixin):

    model = Course
    template_name = 'quiz/dashboard/profile.html'

    def get_queryset(self):
        return Course.objects.all()
        
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        context['course_count'] =QMODEL.Course.objects.all().count()
        context['question_count'] =QMODEL.Question.objects.all().count()
        context['result_count'] =QMODEL.Result.objects.all().count()
        context['student_count'] = Student.objects.all().count()
        context['student'] = Student.objects.get(user_id=self.request.user.id)
        return context

# quiz app views

@login_required
def userprofileview(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    # student = Profile.objects.get(user_id=request.user.id)
    student = request.user.id  
    # m = QMODEL.Result.objects.aggregate(Max('marks'))  
    max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    results = Result.objects.filter(id = Subquery(max_q[:1]), exam=course, student = student)
    Result.objects.filter(id__in = Subquery(max_q[1:]), exam=course)
    user_profile =  Student.objects.filter(user_id = request.user)

    # results=QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
              
    context = {
        'results':results,
        'course':course,
        'st':request.user,
        'user_profile':user_profile 
    }
    return render(request,'sms/profile.html', context)

class UserProfileForm(LoginRequiredMixin, CreateView):
    models = Student
    fields = '__all__'
    template_name = 'sms/userprofileform.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True

    def get_queryset(self):
        return Student.objects.all()

class UserProfileUpdateForm(LoginRequiredMixin, UpdateView):
    models = Student
    fields = '__all__'
    template_name = 'sms/userprofileupdateform.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True

    def get_queryset(self):
        return Student.objects.all()

# admin result view

class Admin_result(LoginRequiredMixin, ListView):
    models = QMODEL.Course
    template_name = 'sms/admin_result.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return QMODEL.Course.objects.all()


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
    return render(request,'sms/Admin_result_detail_view.html', context)

@login_required
def take_exams_view(request):
    course = QMODEL.Course.objects.all()
    context = {
        'courses':course
    }
    return render(request, 'quiz/take_exams.html', context=context)

@login_required
def start_exams_view(request, pk):

    course = QMODEL.Course.objects.get(id = pk)
    # questions = QMODEL.Question.objects.all().filter(course = course).order_by('?')
    questions = QMODEL.Question.objects.all().filter(course = course)

    q_count = QMODEL.Question.objects.all().filter(course = course).count()   
    paginator = Paginator(questions, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'course':course,
        'questions':questions,
        'q_count':q_count,
        'page_obj':page_obj
    }
    if request.method == 'POST':
        pass
    response = render(request, 'quiz/start_exams.html', context=context)
    response.set_cookie('course_id', course.id)
    return response

@login_required
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view_result')
    else:
        return HttpResponseRedirect('take-exam')

@login_required
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'quiz/view_result.html',{'courses':courses})


from django.db.models import Count

@login_required
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = Student.objects.all()
 
    context = {
        'results':student,
        'course':course,
        'st':request.user,
        
    }
    return render(request,'quiz/check_marks.html', context)

class InstructionListView(ListView, LoginRequiredMixin):
    model = Course
    template_name = 'quiz/intruction.html'
    
    def get_queryset(self):
        return Course.objects.all()