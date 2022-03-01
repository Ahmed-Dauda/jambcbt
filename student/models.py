from django.db import models
# from users.models import NewUser
from django.contrib.auth.models import User
from django.conf import settings


class Student(models.Model):
    dept_choice = [
        ('science', 'science'),
        ('Art', 'Art'),
        
     ]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    first_name = models.CharField(max_length=40, blank=True,  null=True)
    last_name = models.CharField(max_length=40, blank=True,  null=True)
    address = models.CharField(max_length=40, blank=True,  null=True)
    age = models.CharField(max_length=40, blank=True,  null=True)
    dept = models.CharField(choices=dept_choice, max_length=20, blank=True,  null=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.first_name}- {self.last_name}"
   


    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

