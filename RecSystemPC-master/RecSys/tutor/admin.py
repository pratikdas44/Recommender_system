from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from tutor.models import Teacher, TeacherFeedback
class TeacherFeedbackAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('STUDENT_NAME', 'COLLEGE_NAME')
    list_filter = ['STUDENT_NAME', 'COLLEGE_NAME']
    search_fields = ['STUDENT_NAME', 'COLLEGE_NAME']
admin.site.register(TeacherFeedback, TeacherFeedbackAdmin)
class TeacherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('TEACHER_NAME', 'id')
admin.site.register(Teacher, TeacherAdmin)
