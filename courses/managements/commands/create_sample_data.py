from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Category, Course, CourseTag
from users.models import InstructorProfile
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for the LMS'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Web Development', 'slug': 'web-development', 'icon': 'code', 'color': '#3B82F6'},
            {'name': 'Data Science', 'slug': 'data-science', 'icon': 'bar-chart', 'color': '#10B981'},
            {'name': 'Cloud Computing', 'slug': 'cloud-computing', 'icon': 'cloud', 'color': '#8B5CF6'},
            {'name': 'Digital Marketing', 'slug': 'digital-marketing', 'icon': 'megaphone', 'color': '#F59E0B'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create tags
        tags_data = ['JavaScript', 'Python', 'React', 'Machine Learning', 'AWS', 'SEO']
        for tag_name in tags_data:
            tag, created = CourseTag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_name.lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(f'Created tag: {tag.name}')
        
        # Create instructor
        instructor, created = User.objects.get_or_create(
            email='instructor@lms.com',
            defaults={
                'username': 'instructor',
                'first_name': 'John',
                'last_name': 'Doe',
                'user_type': 'instructor',
                'is_active': True,
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()
            
            # Create instructor profile
            InstructorProfile.objects.create(
                user=instructor,
                expertise_areas='Web Development, JavaScript, React',
                years_of_experience=5,
                education='Computer Science Degree',
                is_verified=True
            )
            self.stdout.write(f'Created instructor: {instructor.email}')
        
        # Create sample course
        web_dev_category = Category.objects.get(slug='web-development')
        course, created = Course.objects.get_or_create(
            slug='complete-web-development',
            defaults={
                'title': 'Complete Web Development Bootcamp',
                'description': 'Learn HTML, CSS, JavaScript, React, and Node.js in this comprehensive course.',
                'short_description': 'Master web development from scratch',
                'instructor': instructor,
                'category': web_dev_category,
                'difficulty_level': 'beginner',
                'duration_hours': 40,
                'price': 89.99,
                'original_price': 199.99,
                'what_you_will_learn': json.dumps([
                    'HTML5 and CSS3',
                    'JavaScript ES6+',
                    'React.js',
                    'Node.js and Express',
                    'Database integration'
                ]),
                'requirements': json.dumps([
                    'Basic computer skills',
                    'No programming experience required'
                ]),
                'target_audience': json.dumps([
                    'Beginners who want to learn web development',
                    'Career changers',
                    'Students'
                ]),
                'status': 'published',
                'is_featured': True,
                'is_bestseller': True,
            }
        )
        if created:
            # Add tags
            js_tag = CourseTag.objects.get(name='JavaScript')
            react_tag = CourseTag.objects.get(name='React')
            course.tags.add(js_tag, react_tag)
            self.stdout.write(f'Created course: {course.title}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))