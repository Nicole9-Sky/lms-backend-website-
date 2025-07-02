from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='user-profile-update'),
    
    # Instructors
    path('instructors/', views.InstructorListView.as_view(), name='instructor-list'),
    path('instructors/<int:pk>/', views.InstructorDetailView.as_view(), name='instructor-detail'),
    path('instructor-profile/', views.InstructorProfileView.as_view(), name='instructor-profile'),
    path('instructor-profile/update/', views.InstructorProfileUpdateView.as_view(), name='instructor-profile-update'),
]

print("✅ User URLs created successfully!")
