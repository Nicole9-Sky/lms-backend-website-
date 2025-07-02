from rest_framework import serializers
from .models import Review
from users.serializers import UserListSerializer
from courses.serializers import CourseListSerializer

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews"""
    
    student = UserListSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'course', 'student', 'rating', 'title', 'comment',
            'is_approved', 'is_featured', 'helpful_count', 'created_at'
        ]
        read_only_fields = ['id', 'student', 'helpful_count', 'created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reviews"""
    
    class Meta:
        model = Review
        fields = ['course', 'rating', 'title', 'comment']
    
    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)