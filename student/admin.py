from django.contrib import admin
from student.models import Student
from quiz.models import Course
from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget
# Register your models here.

admin.site.register(Student)
class BookResource(resources.ModelResource):
    # from_encoding = 'latin-1'
    class Meta:
        model = Course

class CourseAdmin(ImportExportModelAdmin):
    resource_class = BookResource

    class Meta:
        model = Course
        # exclude = ('id','course' )

admin.site.register(Course, CourseAdmin)
