from django.contrib import admin
from .models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_featured', 'created_at']
    search_fields = ['student__username', 'course__title', 'title']
    readonly_fields = ['created_at', 'helpful_count']