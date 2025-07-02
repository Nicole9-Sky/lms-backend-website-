from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Course
from enrollments.models import Enrollment
from reviews.models import Review
from users.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instructor_dashboard(request):
    """Get instructor dashboard data"""
    
    if request.user.user_type != 'instructor':
        return Response({'error': 'Not an instructor'}, status=403)
    
    courses = Course.objects.filter(instructor=request.user)
    enrollments = Enrollment.objects.filter(course__instructor=request.user)
    
    # Calculate stats
    stats = {
        'total_courses': courses.count(),
        'published_courses': courses.filter(status='published').count(),
        'draft_courses': courses.filter(status='draft').count(),
        'total_students': enrollments.values('student').distinct().count(),
        'total_enrollments': enrollments.count(),
        'active_enrollments': enrollments.filter(status='active').count(),
        'completed_enrollments': enrollments.filter(status='completed').count(),
        'total_revenue': enrollments.aggregate(
            total=Sum('amount_paid')
        )['total'] or 0,
        'average_rating': Review.objects.filter(
            course__instructor=request.user
        ).aggregate(avg=Avg('rating'))['avg'] or 0,
        'total_reviews': Review.objects.filter(
            course__instructor=request.user
        ).count(),
    }
    
    # Recent activity
    recent_enrollments = enrollments.order_by('-enrolled_at')[:5].values(
        'student__first_name', 'student__last_name', 'course__title', 
        'enrolled_at', 'amount_paid'
    )
    
    recent_reviews = Review.objects.filter(
        course__instructor=request.user
    ).order_by('-created_at')[:5].values(
        'student__first_name', 'student__last_name', 'course__title',
        'rating', 'title', 'created_at'
    )
    
    # Monthly revenue (last 6 months)
    monthly_revenue = []
    for i in range(6):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        revenue = enrollments.filter(
            enrolled_at__range=[month_start, month_end]
        ).aggregate(total=Sum('amount_paid'))['total'] or 0
        
        monthly_revenue.append({
            'month': month_start.strftime('%B %Y'),
            'revenue': float(revenue)
        })
    
    return Response({
        'stats': stats,
        'recent_enrollments': list(recent_enrollments),
        'recent_reviews': list(recent_reviews),
        'monthly_revenue': monthly_revenue[::-1]  # Reverse to show oldest first
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):
    """Get student dashboard data"""
    
    enrollments = Enrollment.objects.filter(student=request.user)
    
    stats = {
        'total_courses': enrollments.count(),
        'active_courses': enrollments.filter(status='active').count(),
        'completed_courses': enrollments.filter(status='completed').count(),
        'certificates_earned': enrollments.filter(certificate_issued=True).count(),
        'total_spent': enrollments.aggregate(
            total=Sum('amount_paid')
        )['total'] or 0,
        'average_progress': enrollments.aggregate(
            avg=Avg('progress_percentage')
        )['avg'] or 0,
    }
    
    # Recent courses
    recent_courses = enrollments.order_by('-last_accessed_at')[:5].values(
        'course__title', 'course__slug', 'progress_percentage', 
        'enrolled_at', 'last_accessed_at', 'status'
    )
    
    # Courses to continue (active with progress < 100%)
    continue_courses = enrollments.filter(
        status='active', progress_percentage__lt=100
    ).order_by('-last_accessed_at')[:3].values(
        'course__title', 'course__slug', 'progress_percentage',
        'course__thumbnail'
    )
    
    return Response({
        'stats': stats,
        'recent_courses': list(recent_courses),
        'continue_courses': list(continue_courses)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    """Get admin dashboard data"""
    
    if not request.user.is_staff:
        return Response({'error': 'Not authorized'}, status=403)
    
    # Overall platform stats
    stats = {
        'total_users': User.objects.count(),
        'total_students': User.objects.filter(user_type='student').count(),
        'total_instructors': User.objects.filter(user_type='instructor').count(),
        'total_courses': Course.objects.count(),
        'published_courses': Course.objects.filter(status='published').count(),
        'total_enrollments': Enrollment.objects.count(),
        'total_revenue': Enrollment.objects.aggregate(
            total=Sum('amount_paid')
        )['total'] or 0,
        'total_reviews': Review.objects.count(),
    }
    
    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5].values(
        'first_name', 'last_name', 'email', 'user_type', 'date_joined'
    )
    
    recent_courses = Course.objects.order_by('-created_at')[:5].values(
        'title', 'instructor__first_name', 'instructor__last_name',
        'status', 'created_at'
    )
    
    # Top performing courses
    top_courses = Course.objects.filter(status='published').annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-enrollment_count')[:5].values(
        'title', 'instructor__first_name', 'instructor__last_name',
        'enrollment_count', 'average_rating'
    )
    
    return Response({
        'stats': stats,
        'recent_users': list(recent_users),
        'recent_courses': list(recent_courses),
        'top_courses': list(top_courses)
    })