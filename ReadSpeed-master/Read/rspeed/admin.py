from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from rspeed.models import ReadSpeed
class ReadSpeedAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('STUDENT_NAME', 'SUBJECT_NAME')
    list_filter = ['STUDENT_NAME', 'SUBJECT_NAME']
    search_fields = ['STUDENT_NAME', 'SUBJECT_NAME']
admin.site.register(ReadSpeed, ReadSpeedAdmin)
