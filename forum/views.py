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
    fields = ['title', 'content', 'category', 'course']

    template_name = 'forum/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
def postView(request, post_id):
    post = Post.objects.get(pk = post_id)
    is_mod = request.user.groups.filter(name='Moderators').count()

    return render(request, 'forum/post.html', context={'post': post, 'is_mod': is_mod})

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

def categoryView(request, cat_slug):
    cat = get_object_or_404(Category, slug=cat_slug)

    return render(request, 'forum/category.html', context={"category": cat, "post_list": cat.post_set.all().order_by('-pk')}) # type: ignore post_set error

def editReply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)

    if request.user == reply.author or request.user.is_staff or request.user.groups.filter(name='Moderators').count():
        if request.method == "POST":
            form = replyForm(request.POST, instance=reply)
            if form.is_valid():
                form.save()
                return redirect('forum:post', post_id=reply.post.pk)
        else:
            form = replyForm(instance=reply)

        return render(request, 'forum/edit_reply.html', {
            'reply': reply, 'form': form, 'post': reply.post,
        })
    
    else:
        return HttpResponse("<h1>You are not allowed here </h1>")
    
def deleteReply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    post_id = reply.post.pk
    
    if reply.author == request.user or request.user.is_staff or request.user.groups.filter(name='Moderators').count():
        reply.is_deleted = True
        reply.save()
        
        return redirect('forum:post', post_id=post_id)
    else:
        return HttpResponse(f"<h1>You are not allowed here f{request.user.username}</h1>")
