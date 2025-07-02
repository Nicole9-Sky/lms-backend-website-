from rest_framework import serializers
from .models import Category, Course, Section, Lesson, CourseTag
from users.serializers import UserListSerializer
import json

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for course categories"""
    
    course_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'course_count']
    
    def get_course_count(self, obj):
        return obj.courses.filter(status='published').count()

class CourseTagSerializer(serializers.ModelSerializer):
    """Serializer for course tags"""
    
    class Meta:
        model = CourseTag
        fields = ['id', 'name', 'slug']

class LessonSerializer(serializers.ModelSerializer):
    """Serializer for lessons"""
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'lesson_type', 'duration_minutes',
            'order', 'is_preview', 'is_mandatory'
        ]

class SectionSerializer(serializers.ModelSerializer):
    """Serializer for course sections"""
    
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Section
        fields = [
            'id', 'title', 'description', 'order',
            'lessons', 'lesson_count', 'total_duration'
        ]
    
    def get_lesson_count(self, obj):
        return obj.lessons.count()
    
    def get_total_duration(self, obj):
        from django.db.models import Sum
        return obj.lessons.aggregate(
            total=Sum('duration_minutes')
        )['total'] or 0

class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for course list view"""
    
    instructor = UserListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = CourseTagSerializer(many=True, read_only=True)
    discount_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description', 'instructor', 'category',
            'difficulty_level', 'duration_hours', 'language', 'price', 'original_price',
            'is_free', 'thumbnail', 'is_bestseller', 'is_featured',
            'total_students', 'average_rating', 'total_reviews',
            'discount_percentage', 'tags', 'created_at'
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer for course detail view"""
    
    instructor = UserListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = CourseTagSerializer(many=True, read_only=True)
    sections = SectionSerializer(many=True, read_only=True)
    discount_percentage = serializers.ReadOnlyField()
    
    # Parse JSON fields
    what_you_will_learn_list = serializers.SerializerMethodField()
    requirements_list = serializers.SerializerMethodField()
    target_audience_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'instructor', 'category', 'difficulty_level', 'duration_hours',
            'language', 'price', 'original_price', 'is_free', 'thumbnail',
            'preview_video', 'what_you_will_learn', 'what_you_will_learn_list',
            'requirements', 'requirements_list', 'target_audience', 'target_audience_list',
            'is_bestseller', 'is_featured', 'total_students', 'average_rating',
            'total_reviews', 'discount_percentage', 'tags', 'sections',
            'created_at', 'published_at'
        ]
    
    def get_what_you_will_learn_list(self, obj):
        try:
            return json.loads(obj.what_you_will_learn) if obj.what_you_will_learn else []
        except json.JSONDecodeError:
            return []
    
    def get_requirements_list(self, obj):
        try:
            return json.loads(obj.requirements) if obj.requirements else []
        except json.JSONDecodeError:
            return []
    
    def get_target_audience_list(self, obj):
        try:
            return json.loads(obj.target_audience) if obj.target_audience else []
        except json.JSONDecodeError:
            return []