from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    dept = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.code} - {self.name}'
    
class Resource(models.Model):
    category_choices = [
        ("PDF", "PDF File"),
        ("Video", "Video Lecture"),
        ("URL", "Link to external resource"), 
    ]

    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.CharField(choices=category_choices, max_length=10, default="URL")

    def __str__(self) -> str:
        return self.title