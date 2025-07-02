from rest_framework import serializers
from .models import Enrollment, LessonProgress
from courses.serializers import CourseListSerializer
from users.serializers import UserListSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for enrollments"""
    
    course = CourseListSerializer(read_only=True)
    student = UserListSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'status', 'enrolled_at', 'completed_at',
            'progress_percentage', 'last_accessed_at', 'amount_paid',
            'certificate_issued', 'certificate_issued_at'
        ]
        read_only_fields = ['id', 'enrolled_at', 'progress_percentage']

class LessonProgressSerializer(serializers.ModelSerializer):
    """Serializer for lesson progress"""
    
    class Meta:
        model = LessonProgress
        fields = [
            'id', 'lesson', 'is_completed', 'completion_percentage',
            'time_spent_minutes', 'started_at', 'completed_at',
            'notes', 'is_bookmarked'
        ]