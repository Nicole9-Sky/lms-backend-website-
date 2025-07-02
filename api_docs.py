from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_documentation(request):
    """Complete API Documentation"""
    
    base_url = request.build_absolute_uri('/api/')
    
    documentation = {
        'version': '1.0',
        'base_url': base_url,
        'authentication': {
            'description': 'JWT Token Authentication',
            'endpoints': {
                'login': {
                    'url': f'{base_url}auth/login/',
                    'method': 'POST',
                    'body': {
                        'email': 'user@example.com',
                        'password': 'password123'
                    },
                    'response': {
                        'access': 'jwt_access_token',
                        'refresh': 'jwt_refresh_token'
                    }
                },
                'refresh': {
                    'url': f'{base_url}auth/refresh/',
                    'method': 'POST',
                    'body': {'refresh': 'jwt_refresh_token'}
                },
                'register': {
                    'url': f'{base_url}users/register/',
                    'method': 'POST',
                    'body': {
                        'username': 'newuser',
                        'email': 'new@example.com',
                        'password': 'password123',
                        'password_confirm': 'password123',
                        'first_name': 'John',
                        'last_name': 'Doe',
                        'user_type': 'student'
                    }
                }
            }
        },
        'courses': {
            'list': {
                'url': f'{base_url}courses/',
                'method': 'GET',
                'filters': {
                    'category_slug': 'web-development',
                    'difficulty_level': 'beginner',
                    'price_min': '0',
                    'price_max': '100',
                    'is_free': 'true',
                    'search': 'javascript'
                }
            },
            'detail': {
                'url': f'{base_url}courses/{{slug}}/',
                'method': 'GET'
            },
            'categories': {
                'url': f'{base_url}courses/categories/',
                'method': 'GET'
            },
            'featured': {
                'url': f'{base_url}courses/lists/featured/',
                'method': 'GET'
            }
        },
        'enrollments': {
            'list': {
                'url': f'{base_url}enrollments/',
                'method': 'GET',
                'auth_required': True
            },
            'enroll': {
                'url': f'{base_url}enrollments/enroll/{{course_slug}}/',
                'method': 'POST',
                'auth_required': True
            }
        },
        'reviews': {
            'list': {
                'url': f'{base_url}reviews/course/{{course_slug}}/',
                'method': 'GET'
            },
            'create': {
                'url': f'{base_url}reviews/course/{{course_slug}}/create/',
                'method': 'POST',
                'auth_required': True,
                'body': {
                    'rating': 5,
                    'title': 'Great course!',
                    'comment': 'I learned a lot from this course.'
                }
            }
        },
        'analytics': {
            'instructor_dashboard': {
                'url': f'{base_url}courses/analytics/instructor-dashboard/',
                'method': 'GET',
                'auth_required': True,
                'user_type': 'instructor'
            },
            'student_dashboard': {
                'url': f'{base_url}courses/analytics/student-dashboard/',
                'method': 'GET',
                'auth_required': True,
                'user_type': 'student'
            }
        }
    }
    
    return Response(documentation)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'version': '1.0',
        'timestamp': request.META.get('HTTP_DATE')
    })