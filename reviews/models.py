from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from courses.models import Course
import uuid

User = get_user_model()

class Review(models.Model):
    """Course reviews and ratings"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    # Review content
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    
    # Review status
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Helpful votes
    helpful_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ['course', 'student']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['course', 'is_approved']),
            models.Index(fields=['student']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.title} ({self.rating}★)"

class ReviewHelpful(models.Model):
    """Track which users found reviews helpful"""
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helpful_reviews')
    is_helpful = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'review_helpful'
        verbose_name = 'Review Helpful Vote'
        verbose_name_plural = 'Review Helpful Votes'
        unique_together = ['review', 'user']
    
    def __str__(self):
        return f"{self.user.full_name} - {self.review.course.title} - {'Helpful' if self.is_helpful else 'Not Helpful'}"

class InstructorReview(models.Model):
    """Reviews specifically for instructors"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_reviews_given')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='instructor_reviews')
    
    # Rating categories
    teaching_quality = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    course_content = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    responsiveness = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2)
    
    # Review content
    comment = models.TextField()
    
    # Status
    is_approved = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'instructor_reviews'
        verbose_name = 'Instructor Review'
        verbose_name_plural = 'Instructor Reviews'
        unique_together = ['instructor', 'student', 'course']
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # Calculate overall rating as average of all categories
        self.overall_rating = (
            self.teaching_quality + self.course_content + self.responsiveness
        ) / 3
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Instructor Review: {self.instructor.full_name} by {self.student.full_name}"

print("✅ Review models created successfully!")
