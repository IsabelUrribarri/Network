
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_post", views.new_post, name="new_post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allPosts", views.allPosts, name="allPosts"),
    path("followingPosts/<int:id>", views.followingPosts, name="followingPosts"),
    path("profile/<int:id>", views.profile, name="profile"),

# API Routes
    path("profile/network", views.follow_unfollow, name="follow_unfollow"),
    path("network/<int:user_id>", views.get_user, name="get_user"), 
]
 