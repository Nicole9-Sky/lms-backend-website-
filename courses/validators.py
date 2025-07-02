from django.core.exceptions import ValidationError
import json
import re

def validate_json_list(value):
    """Validate that the value is a valid JSON list"""
    try:
        data = json.loads(value)
        if not isinstance(data, list):
            raise ValidationError('Must be a valid JSON list')
        if len(data) > 20:
            raise ValidationError('List cannot have more than 20 items')
    except json.JSONDecodeError:
        raise ValidationError('Must be valid JSON')

def validate_price(value):
    """Validate course price"""
    if value < 0:
        raise ValidationError('Price cannot be negative')
    if value > 10000:
        raise ValidationError('Price cannot exceed $10,000')

def validate_slug(value):
    """Validate slug format"""
    if not re.match(r'^[a-z0-9-]+$', value):
        raise ValidationError('Slug can only contain lowercase letters, numbers, and hyphens')
    if len(value) < 3:
        raise ValidationError('Slug must be at least 3 characters long')

def validate_video_url(value):
    """Validate video URL"""
    if value and not (value.startswith('http://') or value.startswith('https://')):
        raise ValidationError('Video URL must start with http:// or https://')