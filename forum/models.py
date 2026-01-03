from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Course, Resource

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    desc = models.TextField()

    def __str__(self):
        return self.name
        
class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, max_length=20, blank=True)

class Reply(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE) 
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Reply to post - {self.post}'
    
    def author_id_extracted(self): # using author_id conflicted with django names
        return self.author.email[1:9]

class Post(models.Model):
    title = models.CharField(max_length=100) # max length is required
    content = models.TextField() # max length not required
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    is_locked = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('forum:home') # replace with the post page

    # extract id from email
    def author_id_extracted(self): # using author_id conflicted with django names
        return self.author.email[1:9]
    
class Report(models.Model):
    statuschoice = [
        ("R", "Resolved"),
        ("P", "Pending"),
        ("X", "Rejected"),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(choices=statuschoice, max_length=15, default="P")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"Report to post - {self.post.title}"
    
    def author_id_extracted(self): # using author_id conflicted with django names
        return self.author.email[1:9]