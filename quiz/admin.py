from dataclasses import Field
from django.contrib import admin
from quiz.models import Course, Question, Result, Timer
# Register your models here.

# admin.site.register(Course)
# admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Timer)

from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget


class BookResource(resources.ModelResource):
    
    course_name = fields.Field(
        column_name='course test',
        attribute='course',
        widget=ForeignKeyWidget(Course,'course_name') )
    
    class Meta:
        model = Question
        # exclude = ('id', )
       
       

class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource

    class Meta:
        model = Question
        # import_id_fields = ('id',)
        
        # exclude = ('id',)

admin.site.register(Question, BookAdmin)

