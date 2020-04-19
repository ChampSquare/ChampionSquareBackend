from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


# Register your models here.

from .models import OfflineExamResultResource, OfflineExamResult, StudentRecordResource, Student


class OfflineResultAdmin(ImportExportModelAdmin):
    resource_class = OfflineExamResultResource


class StudentRecordAdmin(ImportExportModelAdmin):
    resource_class = StudentRecordResource


admin.site.register(OfflineExamResult, OfflineResultAdmin)
admin.site.register(Student, StudentRecordAdmin)

