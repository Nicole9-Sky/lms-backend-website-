from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    
    USER_TYPES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Professional information
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    
    # Learning preferences
    preferred_language = models.CharField(max_length=50, default='English')
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

class InstructorProfile(models.Model):
    """Extended profile for instructors"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    expertise_areas = models.TextField(help_text="Comma-separated list of expertise areas")
    years_of_experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    teaching_experience = models.TextField(blank=True)
    
    # Social proof
    total_students = models.PositiveIntegerField(default=0)
    total_courses = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'instructor_profiles'
        verbose_name = 'Instructor Profile'
        verbose_name_plural = 'Instructor Profiles'
    
    def __str__(self):
        return f"Instructor: {self.user.full_name}"