from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    # Enrollments
    path('', views.EnrollmentListView.as_view(), name='enrollment-list'),
    path('<uuid:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('enroll/<slug:course_slug>/', views.enroll_course, name='enroll-course'),
    
    # Progress tracking
    path('<uuid:enrollment_id>/lessons/<int:lesson_id>/progress/', 
         views.update_lesson_progress, name='update-lesson-progress'),
]