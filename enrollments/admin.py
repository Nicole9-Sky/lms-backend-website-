from django.contrib import admin
from .models import Enrollment, LessonProgress

# Register your models here.
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'progress_percentage', 'enrolled_at']
    list_filter = ['status', 'enrolled_at', 'certificate_issued']
    search_fields = ['student__username', 'course__title']
    readonly_fields = ['enrolled_at', 'progress_percentage']

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'is_completed', 'completion_percentage']
    list_filter = ['is_completed', 'is_bookmarked']
    search_fields = ['enrollment__student__username', 'lesson__title']