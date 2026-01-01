from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.home, name="home"),
    path('new/', views.newPost.as_view(), name="create"),
    path('post/<int:post_id>', views.postView, name="post"),
    path('post/<int:post_id>/reply', views.newReply, name='reply'),
    path('category/<str:cat_slug>', views.categoryView, name="category"),
    path('reply/<int:reply_id>/edit', views.editReply, name='editreply'),
    path('reply/<int:reply_id>/delete', views.deleteReply, name='deletereply'),
]