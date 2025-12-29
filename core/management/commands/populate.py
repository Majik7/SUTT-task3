from core.models import Course, Resource
from forum.models import Category
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

# this is temporary i might scrape the data from somewhere if time permits
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # for courses
        course_list = [
            {"code": "CSF101", "name": "Introduction to Computer Programming", "dept": "Computer Science"},
            {"code": "BITSF111", "name": "Thermodynamics", "dept": "Mechanical"},
            {"code": "BITSK101", "name": "Physical Health & Wellbeing", "dept": "Physical Education"},
            {"code": "BIOF101", "name": "Introduction to Biological Sciences", "dept": "Biology"},
            {"code": "MATHF101", "name": "Multivariable Calculus", "dept": "Mathematics"},
            {"code": "BITSF103", "name": "Engineering Design and Prototype", "dept": "Civil"},
            {"code": "BITSF101", "name": "Social Conduct", "dept": "idk"},
        ]

        for course_data in course_list:
            if Course.objects.filter(code = course_data['code']):
                print(f"Course {course_data['code']} - {course_data['name']} already exists, skipping")
                continue
            else:
                course_obj = Course.objects.create(
                    code = course_data['code'],
                    name = course_data['name'],
                    dept = course_data['dept'],
                )

                # for resources
                Resource.objects.create(
                    course = course_obj,
                    title = f"Sample resource for course {course_obj.code}",
                )

                print(f"Added course {course_data['code']}")

        # for categories
        category_list = [
            {"name": "General Queries", "slug": "general-queries", "desc": "General Queries"},
            {"name": "Doubts", "slug": "doubts", "desc": "To ask doubts"},
            {"name": "Resource Request", "slug": "resource-request", "desc": "Ask for resources"},
        ]

        for category in category_list:
            if Category.objects.filter(slug = category['slug']):
                print(f"Category {category['name']} already exists, skipping")
                continue
            else:
                Category.objects.create(
                    name = category['name'],
                    slug = category['slug'],
                    desc = category['desc'],
                )

                print(f"added category {category['name']}")