from django.urls import path
from . import views, analytics

app_name = 'courses'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Courses
    path('', views.CourseListView.as_view(), name='course-list'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course-detail'),
    
    # Statistics and special lists
    path('stats/overview/', views.course_stats, name='course-stats'),
    path('lists/featured/', views.featured_courses, name='featured-courses'),
    path('lists/bestsellers/', views.bestseller_courses, name='bestseller-courses'),
    path('lists/popular/', views.popular_courses, name='popular-courses'),

    # Analytics
    path('analytics/instructor-dashboard/', analytics.instructor_dashboard, name='instructor-dashboard'),
    path('analytics/student-dashboard/', analytics.student_dashboard, name='student-dashboard'),
    path('analytics/admin-dashboard/', analytics.admin_dashboard, name='admin-dashboard'),
]

print("✅ Course URLs created successfully!")
