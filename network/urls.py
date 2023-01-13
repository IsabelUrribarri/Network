
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_post", views.new_post, name="new_post"),
    path("update_post/<int:id>", views.update_post, name="update_post"),
    path("<int:post_id>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allPosts", views.allPosts, name="allPosts"),
    path("followingPosts/<int:id>", views.followingPosts, name="followingPosts"),
    path("profile/<int:id>", views.profile, name="profile"),

# API Routes
    path("profile/network", views.follow_unfollow, name="follow_unfollow"),
    path("network/<int:post_id>", views.get_post, name="get_post"), 
    path("network/like/<int:post_id>", views.toggle_like, name="toggle_like"),
]
 