from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.home, name="home"),
    path('new/', views.newPost.as_view(), name="create"),
    path('<int:post_id>', views.postView, name="post"),
    path('reply/<int:post_id>', views.newReply, name='reply'),
]