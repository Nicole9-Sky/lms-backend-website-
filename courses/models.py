from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Create your models here.
User = get_user_model()

class Category(models.Model):
    """Course categories"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name")
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Course(models.Model):
    """Main course model"""
    
    DIFFICULTY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    
    # Relationships
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    
    # Course Details
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration_hours = models.PositiveIntegerField(help_text="Total course duration in hours")
    language = models.CharField(max_length=50, default='English')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_free = models.BooleanField(default=False)
    
    # Media
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    preview_video = models.URLField(blank=True, help_text="Preview video URL")
    
    # Course Features
    what_you_will_learn = models.TextField(blank=True, help_text="JSON array of learning outcomes")
    requirements = models.TextField(blank=True, help_text="Course requirements")
    target_audience = models.TextField(blank=True, help_text="Who this course is for")
    
    # Status and Flags
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Statistics (updated via signals)
    total_students = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['category', 'difficulty_level']),
            models.Index(fields=['price', 'is_free']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

class Section(models.Model):
    """Course sections/modules"""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sections'
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = ['course', 'order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    """Individual lessons within sections"""
    
    LESSON_TYPES = (
        ('video', 'Video'),
        ('text', 'Text'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('resource', 'Resource'),
    )
    
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='video')
    content = models.TextField(blank=True, help_text="Lesson content or video URL")
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    
    # Lesson settings
    is_preview = models.BooleanField(default=False, help_text="Can be viewed without enrollment")
    is_mandatory = models.BooleanField(default=True)
    
    # File attachments
    video_file = models.FileField(upload_to='lesson_videos/', blank=True, null=True)
    attachments = models.FileField(upload_to='lesson_attachments/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lessons'
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['section', 'order']
        unique_together = ['section', 'order']
    
    def __str__(self):
        return f"{self.section.title} - {self.title}"

class CourseTag(models.Model):
    """Tags for courses"""
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'course_tags'
        verbose_name = 'Course Tag'
        verbose_name_plural = 'Course Tags'
        ordering = ['name']
    
    def __str__(self):
        return self.name

# Many-to-many relationship for course tags
Course.add_to_class('tags', models.ManyToManyField(CourseTag, blank=True, related_name='courses'))

print("✅ Course models created successfully!")
