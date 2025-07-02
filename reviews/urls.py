from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Course reviews
    path('course/<slug:course_slug>/', views.ReviewListView.as_view(), name='course-reviews'),
    path('course/<slug:course_slug>/create/', views.ReviewCreateView.as_view(), name='create-review'),
    path('course/<slug:course_slug>/stats/', views.course_reviews_stats, name='course-review-stats'),
    
    # User reviews
    path('my-reviews/', views.UserReviewsView.as_view(), name='user-reviews'),
]