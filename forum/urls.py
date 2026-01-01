from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.home, name="home"),

    # post
    path('post/<int:post_id>', views.postView, name="post"),
    path('post/<int:post_id>/reply', views.newReply, name='reply'),
    path('post/<int:post_id>/lock', views.lockPost, name='lock_post'),
    path('post/<int:post_id>/unlock', views.unlockPost, name='unlock_post'),
    path('post/<int:post_id>/report', views.reportPost, name='report_post'),
    path('post/new', views.createPost, name='create_post'),
    path('post/new/<int:category_id>', views.createPostWCat, name='create_post_cat'),
    path('post/<int:post_id>/delete', views.deletePost, name='delete_post'),
    path('post/<int:post_id>/like', views.likePost, name='like_post'),

    # reply
    path('reply/<int:reply_id>/edit', views.editReply, name='editreply'),
    path('reply/<int:reply_id>/delete', views.deleteReply, name='deletereply'),

    # report
    path('reports/post/<int:post_id>', views.viewPostReports, name='view_post_reports'),
    path('reports/resolve/<int:report_id>', views.resolveReport, name='resolve_report'),

    # category
    path('category/<str:cat_slug>', views.categoryView, name="category"),

    # profile
    path('profile/<int:profile_id>', views.profileView, name='profile'),
]