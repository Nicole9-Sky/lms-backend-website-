from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import InstructorProfile
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer,
    InstructorProfileSerializer, UserListSerializer
)
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

User = get_user_model()

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST'), name='post')
class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserProfileView(generics.RetrieveAPIView):
    """Get current user profile"""
    
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserProfileUpdateView(generics.UpdateAPIView):
    """Update current user profile"""
    
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class InstructorListView(generics.ListAPIView):
    """List all instructors"""
    
    serializer_class = InstructorProfileSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return InstructorProfile.objects.filter(
            user__user_type='instructor'
        ).select_related('user').order_by('-average_rating', '-total_students')

class InstructorDetailView(generics.RetrieveAPIView):
    """Get instructor details"""
    
    serializer_class = InstructorProfileSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return InstructorProfile.objects.filter(
            user__user_type='instructor'
        ).select_related('user')

class InstructorProfileView(generics.RetrieveAPIView):
    """Get current instructor profile"""
    
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        try:
            return self.request.user.instructor_profile
        except InstructorProfile.DoesNotExist:
            # Create profile if it doesn't exist
            return InstructorProfile.objects.create(user=self.request.user)

class InstructorProfileUpdateView(generics.UpdateAPIView):
    """Update current instructor profile"""
    
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        profile, created = InstructorProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

print("✅ User views created successfully!")
