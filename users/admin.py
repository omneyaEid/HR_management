from django.contrib import admin
from .models import *
# Register your models here.
class AttendanceAdmin(admin.ModelAdmin):
    list_display=('user','check_in','check_out')
class AttendanceReviewAdmin(admin.ModelAdmin):
    list_display=('user','check_in_late','check_out_early','day')
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(ReviewAttendance,AttendanceReviewAdmin)



