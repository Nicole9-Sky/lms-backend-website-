from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from courses.models import Course

class ReviewListView(generics.ListAPIView):
    """List reviews for a course"""
    
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        return Review.objects.filter(
            course__slug=course_slug,
            is_approved=True
        ).select_related('student', 'course').order_by('-created_at')

class ReviewCreateView(generics.CreateAPIView):
    """Create a review for a course"""
    
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug)
        serializer.save(student=self.request.user, course=course)

class UserReviewsView(generics.ListAPIView):
    """List user's reviews"""
    
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(
            student=self.request.user
        ).select_related('course').order_by('-created_at')

@api_view(['GET'])
@permission_classes([AllowAny])
def course_reviews_stats(request, course_slug):
    """Get review statistics for a course"""
    
    course = get_object_or_404(Course, slug=course_slug)
    reviews = Review.objects.filter(course=course, is_approved=True)
    
    stats = {
        'total_reviews': reviews.count(),
        'average_rating': reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0,
        'rating_distribution': {
            '5': reviews.filter(rating=5).count(),
            '4': reviews.filter(rating=4).count(),
            '3': reviews.filter(rating=3).count(),
            '2': reviews.filter(rating=2).count(),
            '1': reviews.filter(rating=1).count(),
        }
    }
    
    return Response(stats)