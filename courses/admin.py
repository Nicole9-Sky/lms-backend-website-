from django.contrib import admin
from .models import Category, Course, Section, Lesson, CourseTag

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'difficulty_level', 'price', 'status', 'is_featured']
    list_filter = ['status', 'difficulty_level', 'category', 'is_featured', 'is_bestseller']
    search_fields = ['title', 'instructor__username', 'category__name']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'course__title']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'lesson_type', 'duration_minutes', 'order']
    list_filter = ['lesson_type', 'is_preview']
    search_fields = ['title', 'section__title']

@admin.register(CourseTag)
class CourseTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}