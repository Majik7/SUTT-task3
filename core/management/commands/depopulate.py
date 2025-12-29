from django.core.management.base import BaseCommand
from core.models import Course, Resource
from forum.models import Category

# use with caution
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # for categories
        category_count = Category.objects.all().count()
        Category.objects.all().delete()
        print(f"Deleted {category_count} categories")

        # for courses
        course_count = Course.objects.all().count()
        resource_count = Resource.objects.all().count()
        
        Course.objects.all().delete()
        
        print(f"Deleted {course_count} courses and {resource_count} linked resources")