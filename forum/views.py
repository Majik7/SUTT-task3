from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Post, Category, Reply, Report, Tag
from core.models import Course, Resource
from .forms import replyForm, reportForm, postForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.text import slugify
from .helpers import send_reply_notification
from django.core.exceptions import PermissionDenied

# Create your views here.
def home(request):
    category_list = Category.objects.all()
    total_posts_count = Category.objects.all().count()
    post_list = Post.objects.all().order_by('-date_posted')
    paginator = Paginator(post_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category_list": category_list,
        "total_posts_count": total_posts_count,
        "post_list": post_list,
        "page_obj": page_obj,
    }
    return render(request, 'forum/home.html', context=context)

def createPostWCat(request, category_id = None):
    initial_data = {}
    if category_id:
        initial_data['category'] = category_id

    if request.method == 'POST':
        form = postForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # for tags
            tag_data = request.POST.get('tags_input', '')
            if tag_data:
                tag_list = [t.strip() for t in tag_data.split(',') if t.strip()]
                for tag_name in tag_list:
                    tag_obj, created = Tag.objects.get_or_create(name=tag_name, defaults={'slug': slugify(tag_name)})
                    post.tags.add(tag_obj)

            return redirect('forum:post', post_id = post.pk)
    else:
        form = postForm(initial=initial_data)

    return render(request, 'forum/create_post.html', {'form': form})

def createPost(request):
    if request.method == 'POST':
        form = postForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # for tags
            tag_data = request.POST.get('tags_input', '') # '' is fallback value
            if tag_data:
                tag_list = [t.strip() for t in tag_data.split(',') if t.strip()]
                for tag_name in tag_list:
                    tag_obj, created = Tag.objects.get_or_create(name=tag_name, defaults={'slug': slugify(tag_name)})
                    post.tags.add(tag_obj)

            return redirect('forum:post', post_id = post.pk)
    else:
        form = postForm()

    return render(request, 'forum/create_post.html', {'form': form})

def deletePost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.author == request.user or request.user.is_staff or request.user.groups.filter(name='Moderators').count():
        post.delete()

        return redirect('forum:home')
    else:
        # return HttpResponse(f"<h1>You are not allowed here {request.user.username}</h1>")
        raise PermissionDenied
    
def likePost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('forum:post', post_id=post_id)
    
def postView(request, post_id):
    post = Post.objects.get(pk = post_id)
    is_mod = request.user.groups.filter(name='Moderators').count()
    report_list = post.report_set.filter(status='P')

    return render(request, 'forum/post.html', context={'post': post, 'is_mod': is_mod, 'report_list': report_list})

def newReply(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.is_locked:
        raise PermissionDenied
    else:
        if request.method == 'POST':
            form = replyForm(request.POST)

            if form.is_valid():
                reply = form.save(commit=False)
                reply.post = post
                reply.author = request.user
                reply.save()

                if post.author.email and post.author != request.user:
                    send_reply_notification(post, reply)

                return redirect('forum:post', post_id = post.pk)
        else:
            form = replyForm()

        return render(request, 'forum/reply.html', {'form': form, 'post': post})

def categoryView(request, cat_slug):
    cat = get_object_or_404(Category, slug=cat_slug)
    post_list = cat.post_set.all().order_by('-pk')
    paginator = Paginator(post_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'forum/category.html', context={"category": cat, "post_list": post_list, "page_obj": page_obj}) # type: ignore post_set error

def editReply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)

    if request.user == reply.author or request.user.is_staff or request.user.groups.filter(name='Moderators').count():
        if request.method == "POST":
            form = replyForm(request.POST, instance=reply) # instance will prefill the fields
            if form.is_valid():
                form.save()
                return redirect('forum:post', post_id=reply.post.pk)
        else:
            form = replyForm(instance=reply)

        return render(request, 'forum/edit_reply.html', {
            'reply': reply, 'form': form, 'post': reply.post,
        })
    
    else:
        # return HttpResponse("<h1>You are not allowed here </h1>")
        raise PermissionDenied
    
def deleteReply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    post_id = reply.post.pk
    
    if reply.author == request.user or request.user.is_staff or request.user.groups.filter(name='Moderators').count():
        reply.is_deleted = True
        reply.save()

        return redirect('forum:post', post_id=post_id)
    else:
        # return HttpResponse(f"<h1>You are not allowed here f{request.user.username}</h1>")
        raise PermissionDenied

    

def profileView(request, profile_id):
    profile_user = get_object_or_404(User, email = f"f{profile_id}@pilani.bits-pilani.ac.in")
    is_mod = profile_user.groups.filter(name='Moderators').count()
    user_posts = profile_user.post_set.all().order_by('-pk') # type: ignore

    paginator = Paginator(user_posts, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'forum/profile.html', context= {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'user_post_count': user_posts.count(),
        'reply_count': profile_user.reply_set.count(), # type: ignore
        'is_mod': is_mod,
        'page_obj': page_obj,
    })

def reportPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = reportForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.post = post
            report.author = request.user
            report.save()
            return redirect('forum:post', post_id = post_id)
    
    else:
        form = reportForm()

    return render(request, 'forum/report_post.html', context={'post': post, 'form': form})

def viewPostReports(request, post_id):
    is_mod = request.user.groups.filter(name='Moderators').count()

    if request.user.is_staff or is_mod:
        post = Post.objects.get(pk = post_id)
        report_list = post.report_set.filter(status='P') # type: ignore
        return render(request, 'forum/view_post_reports.html', context={'post': post, 'is_mod': is_mod, 'report_list': report_list})
    
    else:
        # return HttpResponse('<h1>You are not allowed here</h1>')
        raise PermissionDenied

    

def resolveReport(request, report_id):
    is_mod = request.user.groups.filter(name='Moderators').count()

    if request.user.is_staff or is_mod:
        report = get_object_or_404(Report, pk=report_id)
        post = report.post
        report.status = 'R'
        report.save()

        return redirect('forum:view_post_reports', post_id = post.pk)
    
    else:
        # return HttpResponse("<h1>You are not allowed here</h1>")
        raise PermissionDenied



def lockPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user.is_staff or request.user.groups.filter(name='Moderators').count():
        post.is_locked = True
        post.save()

        return redirect('forum:post', post_id = post_id)
    
    else:
        # return HttpResponse("<h1>You are not allowed here</h1>")
        raise PermissionDenied

    
def unlockPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user.is_staff or request.user.groups.filter(name='Moderators').count():
        post.is_locked = False
        post.save()

        return redirect('forum:post', post_id = post_id)
    
    else:
        # return HttpResponse("<h1>You are not allowed here</h1>")
        raise PermissionDenied

    
def courseView(request, course_code):
    course = get_object_or_404(Course, code=course_code)
    post_list = course.post_set.all().order_by('-pk')
    resource_list = course.resource_set.all()

    paginator = Paginator(post_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'forum/course.html', context={
        'post_list': post_list,
        'resource_list': resource_list,
        'page_obj': page_obj,
        'course': course,
    })


def tagView(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    post_list = tag.post_set.all().order_by('-pk')

    paginator = Paginator(post_list, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'forum/tag.html', context={
        'post_list': post_list,
        'page_obj': page_obj,
        'tag': tag,
    })