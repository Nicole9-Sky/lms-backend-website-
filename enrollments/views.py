from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Enrollment, LessonProgress
from .serializers import EnrollmentSerializer, LessonProgressSerializer
from courses.models import Course


class EnrollmentListView(generics.ListAPIView):
    """List user's enrollments"""
    
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user
        ).select_related('course', 'course__instructor', 'course__category')

class EnrollmentDetailView(generics.RetrieveAPIView):
    """Get enrollment details"""
    
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user
        ).select_related('course', 'course__instructor', 'course__category')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, course_slug):
    """Enroll in a course"""
    
    course = get_object_or_404(Course, slug=course_slug, status='published')
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        return Response(
            {'error': 'Already enrolled in this course'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create enrollment
    enrollment = Enrollment.objects.create(
        student=request.user,
        course=course,
        amount_paid=course.price if not course.is_free else 0
    )
    
    serializer = EnrollmentSerializer(enrollment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_lesson_progress(request, enrollment_id, lesson_id):
    """Update lesson progress"""
    
    enrollment = get_object_or_404(
        Enrollment, 
        id=enrollment_id, 
        student=request.user
    )
    
    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson_id=lesson_id,
        defaults={
            'completion_percentage': request.data.get('completion_percentage', 0),
            'is_completed': request.data.get('is_completed', False),
            'time_spent_minutes': request.data.get('time_spent_minutes', 0),
        }
    )
    
    if not created:
        progress.completion_percentage = request.data.get('completion_percentage', progress.completion_percentage)
        progress.is_completed = request.data.get('is_completed', progress.is_completed)
        progress.time_spent_minutes += request.data.get('time_spent_minutes', 0)
        progress.save()
    
    # Update overall enrollment progress
    enrollment.calculate_progress()
    
    serializer = LessonProgressSerializer(progress)
    return Response(serializer.data)
