from django.contrib import admin
from quiz.models import Course, Question, Result
# Register your models here.

# admin.site.register(Course)
# admin.site.register(Question)
admin.site.register(Result)

from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget


class BookResource(resources.ModelResource):
    course_name = fields.Field(
        column_name='Subject Title',
        attribute='course',
        widget=ForeignKeyWidget(Course,'course_name') )
    # from_encoding = 'latin-1'
    class Meta:
        model = Question
        # exclude = ('id','course' )
       

class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    # from_encoding = 'latin-1'
    class Meta:
        model = Question
        # exclude = ('id','course' )

admin.site.register(Question, BookAdmin)

