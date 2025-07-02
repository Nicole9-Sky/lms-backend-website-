from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson
import uuid

User = get_user_model()

class Enrollment(models.Model):
    """Student course enrollments"""
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    
    # Enrollment details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Progress tracking
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_accessed_at = models.DateTimeField(blank=True, null=True)
    
    # Payment information
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    # Certificates
    certificate_issued = models.BooleanField(default=False)
    certificate_issued_at = models.DateTimeField(blank=True, null=True)
    certificate_url = models.URLField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'enrollments'
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        unique_together = ['student', 'course']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['course', 'status']),
            models.Index(fields=['enrolled_at']),
        ]
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}"
    
    def calculate_progress(self):
        """Calculate and update progress percentage"""
        total_lessons = self.course.sections.aggregate(
            total=models.Count('lessons')
        )['total'] or 0
        
        if total_lessons == 0:
            return 0
        
        completed_lessons = self.lesson_progress.filter(is_completed=True).count()
        progress = (completed_lessons / total_lessons) * 100
        
        self.progress_percentage = round(progress, 2)
        self.save(update_fields=['progress_percentage'])
        
        return self.progress_percentage

class LessonProgress(models.Model):
    """Track individual lesson progress"""
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progress')
    
    # Progress tracking
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_accessed_at = models.DateTimeField(auto_now=True)
    
    # Notes and bookmarks
    notes = models.TextField(blank=True)
    is_bookmarked = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'lesson_progress'
        verbose_name = 'Lesson Progress'
        verbose_name_plural = 'Lesson Progress'
        unique_together = ['enrollment', 'lesson']
        indexes = [
            models.Index(fields=['enrollment', 'is_completed']),
            models.Index(fields=['lesson', 'is_completed']),
        ]
    
    def __str__(self):
        return f"{self.enrollment.student.full_name} - {self.lesson.title}"

class Certificate(models.Model):
    """Course completion certificates"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    
    # Certificate details
    certificate_number = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    # Verification
    verification_code = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=True)
    
    # File storage
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    class Meta:
        db_table = 'certificates'
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"Certificate - {self.enrollment.student.full_name} - {self.enrollment.course.title}"

print("✅ Enrollment models created successfully!")
