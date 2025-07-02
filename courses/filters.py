import django_filters
from django.db import models
from .models import Course, Category

class CourseFilter(django_filters.FilterSet):
    """Filter set for courses"""
    
    # Price filters
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_free = django_filters.BooleanFilter(field_name='is_free')
    
    # Category filters
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    category_slug = django_filters.CharFilter(field_name='category__slug')
    
    # Difficulty level
    difficulty_level = django_filters.ChoiceFilter(choices=Course.DIFFICULTY_LEVELS)
    
    # Duration filters
    duration_min = django_filters.NumberFilter(field_name='duration_hours', lookup_expr='gte')
    duration_max = django_filters.NumberFilter(field_name='duration_hours', lookup_expr='lte')
    
    # Rating filter
    rating_min = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    
    # Language filter
    language = django_filters.CharFilter(field_name='language', lookup_expr='icontains')
    
    # Special filters
    is_bestseller = django_filters.BooleanFilter(field_name='is_bestseller')
    is_featured = django_filters.BooleanFilter(field_name='is_featured')
    
    # Instructor filter
    instructor = django_filters.CharFilter(method='filter_instructor')
    
    class Meta:
        model = Course
        fields = [
            'price_min', 'price_max', 'is_free', 'category', 'category_slug',
            'difficulty_level', 'duration_min', 'duration_max', 'rating_min',
            'language', 'is_bestseller', 'is_featured', 'instructor'
        ]
    
    def filter_instructor(self, queryset, name, value):
        """Filter by instructor name"""
        return queryset.filter(
            models.Q(instructor__first_name__icontains=value) |
            models.Q(instructor__last_name__icontains=value) |
            models.Q(instructor__username__icontains=value)
        )

print("✅ Course filters created successfully!")
