from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Post, Category

dummy_threads = [
        {
            'title': 'How to configure AllAuth with BITS Email?',
            'content': 'I am getting a redirect error when trying to login...',
            'author': {'username': 'sutt_recruit'}, # Nested dict to mimic author.username
            'created_at': datetime.now(),
            'views_count': 120,
            'replies_count': 5, # Note: using an integer directly for now
            'likes_count': 12,
        },
        {
            'title': 'Best resources for CS F213?',
            'content': 'Does anyone have the link to the 2024 handouts?',
            'author': {'username': 'topper_stud'},
            'created_at': datetime.now(),
            'views_count': 45,
            'replies_count': 0,
            'likes_count': 2,
        },
        {
            'title': 'Lost ID Card in the Library',
            'content': 'Found a card near the reference section...',
            'author': {'username': 'librarian'},
            'created_at': datetime.now(),
            'views_count': 10,
            'replies_count': 1,
            'likes_count': 0,
        }
    ]

# Create your views here.
def home(request):
    category_list = Category.objects.all()
    total_posts_count = Category.objects.all().count()
    post_list = Post.objects.all().order_by('-date_posted')

    context = {
        "category_list": category_list,
        "total_posts_count": total_posts_count,
        "post_list": post_list,
    }
    return render(request, 'forum/home.html', context=context)

class newPost(CreateView, LoginRequiredMixin):
    model = Post
    fields = ['title', 'content', 'category']

    template_name = 'forum/create.html'

    

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
def postView(request, post_id):
    post = Post.objects.get(pk = post_id)

    return render(request, 'forum/post.html', context={"post": post})
