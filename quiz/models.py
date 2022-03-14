from django.db import models
from student.models import Student
# from users.models import Profile
from cloudinary.models import CloudinaryField

class Course(models.Model):
   course_name = models.CharField(max_length=50, unique= True)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   id = models.AutoField(primary_key=True)
   
   def __str__(self):
        return f'{self.course_name}'

class Question(models.Model):
    
    course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True, null = True)
    marks=models.PositiveIntegerField()
    question=models.TextField(blank=True, null = True)
    img_quiz = CloudinaryField('image', blank=True, null= True)
    option1=models.CharField(max_length=500, blank=True, null = True)
    option2=models.CharField(max_length=500, blank=True, null = True)
    option3=models.CharField(max_length=500, blank=True, null = True)
    option4=models.CharField(max_length=500, blank=True, null = True)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=500,choices=cat)
    id = models.AutoField(primary_key=True)
    

    def __str__(self):
        return f"{self.course} | {self.question}"

class Timer(models.Model):

    min = models.PositiveIntegerField(default=35)
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f"{self.min}"

class Result(models.Model):

    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return f"{self.student}"


