
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("following", views.following, name="following"),
    path("<str:username>", views.profile, name="profile"),
    path("<str:username>/follow", views.follow, name="follow"),
    path("<str:username>/unfollow", views.unfollow, name="unfollow"),
    path("posts/<int:post_id>", views.post_detail, name="post_detail"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
]
