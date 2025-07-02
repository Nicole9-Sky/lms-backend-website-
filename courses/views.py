from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from .models import Category, Course, Section, Lesson
from .serializers import (
    CategorySerializer, CourseListSerializer, CourseDetailSerializer, 
    SectionSerializer, LessonSerializer
)
from .filters import CourseFilter

class CategoryListView(generics.ListAPIView):
    """List all active categories"""
    
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CourseListView(generics.ListAPIView):
    """List courses with filtering and search"""
    
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'instructor__first_name', 'instructor__last_name']
    filterset_class = CourseFilter
    ordering_fields = ['created_at', 'price', 'average_rating', 'total_students']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Course.objects.filter(status='published').select_related(
            'instructor', 'category'
        ).prefetch_related('tags')

class CourseDetailView(generics.RetrieveAPIView):
    """Get course details"""
    
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Course.objects.filter(status='published').select_related(
            'instructor', 'category'
        ).prefetch_related('tags', 'sections__lessons')

@api_view(['GET'])
@permission_classes([AllowAny])
def course_stats(request):
    """Get overall course statistics"""
    
    stats = {
        'total_courses': Course.objects.filter(status='published').count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_instructors': Course.objects.filter(status='published').values('instructor').distinct().count(),
        'average_course_rating': Course.objects.filter(status='published').aggregate(
            avg_rating=Avg('average_rating')
        )['avg_rating'] or 0,
    }
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_courses(request):
    """Get featured courses"""
    
    courses = Course.objects.filter(
        status='published', is_featured=True
    ).select_related('instructor', 'category').prefetch_related('tags')[:6]
    
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def bestseller_courses(request):
    """Get bestseller courses"""
    
    courses = Course.objects.filter(
        status='published', is_bestseller=True
    ).select_related('instructor', 'category').prefetch_related('tags')[:6]
    
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def popular_courses(request):
    """Get most popular courses by enrollment"""
    
    courses = Course.objects.filter(
        status='published'
    ).select_related('instructor', 'category').prefetch_related('tags').order_by(
        '-total_students'
    )[:6]
    
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)