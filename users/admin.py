from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, InstructorProfile

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_active']
    list_filter = ['user_type', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'profile_picture', 'bio', 'date_of_birth', 'phone_number')
        }),
        ('Professional Info', {
            'fields': ('job_title', 'company', 'website', 'linkedin_profile')
        }),
        ('Preferences', {
            'fields': ('preferred_language', 'timezone')
        }),
    )

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'years_of_experience', 'total_students', 'total_courses', 'average_rating', 'is_verified']
    list_filter = ['is_verified', 'is_featured']
    search_fields = ['user__username', 'user__email', 'expertise_areas']