from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Post, Category, Reply
from .forms import replyForm

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

def newReply(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = replyForm(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.author = request.user
            reply.save()
            return redirect('forum:post', post_id = post.pk)
    else:
        form = replyForm()

    return render(request, 'forum/reply.html', {'form': form, 'post': post})
