from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20)
    desc = models.TextField()

    def __str__(self):
        return self.name
        
class Tag(models.Model):
    name = models.CharField(max_length=20)

class Reply(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE) 

    def __str__(self) -> str:
        return f'Reply to post - {self.post}'

class Post(models.Model):
    title = models.CharField(max_length=100) # max length is required
    content = models.TextField() # max length not required
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    # tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('forum:home') # replace with the post page

    # extract id from email
    def author_id_extracted(self): # using author_id conflicted with django names
        return self.author.email[1:9]
