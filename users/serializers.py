from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import InstructorProfile

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'user_type'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        
        # Create instructor profile if user is instructor
        if validated_data.get('user_type') == 'instructor':
            InstructorProfile.objects.create(user=user)
        
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'user_type', 'profile_picture', 'bio', 'date_of_birth', 'phone_number',
            'job_title', 'company', 'website', 'linkedin_profile',
            'preferred_language', 'timezone', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'username', 'email', 'user_type', 'date_joined', 'last_login']

class InstructorProfileSerializer(serializers.ModelSerializer):
    """Serializer for instructor profile"""
    
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = InstructorProfile
        fields = [
            'user', 'expertise_areas', 'years_of_experience', 'education',
            'certifications', 'teaching_experience', 'total_students',
            'total_courses', 'average_rating', 'is_verified', 'is_featured'
        ]
        read_only_fields = ['total_students', 'total_courses', 'average_rating']

class UserListSerializer(serializers.ModelSerializer):
    """Simplified serializer for user lists"""
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'profile_picture', 'user_type']

print("✅ User serializers created successfully!")
