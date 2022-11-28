from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import date, datetime

from .models import User, Post, UserFollowing

def ifFollowing(following, follower):
    result = following.following.filter(following_user_id=follower)
    if result.count() > 0:
        return 'Unfollow'
    else: 
        return 'Follow'

def index(request):
    return render(request, "network/index.html", {
           "posts": Post.objects.all().order_by('-date_creation'),
           "show_new_post": True
        })

def allPosts(request):
    return render(request, "network/index.html", {
           "posts": Post.objects.all().order_by('-date_creation'),
           "show_new_post": False,
           "title": "All Posts"
        })
def followingPosts(request, id):
    user = User.objects.get(id=id)
    max = UserFollowing.objects.filter(user_id=user).count()
    count = max
    mydata = None
    for following in UserFollowing.objects.filter(user_id=id):
        if count == max:
            mydata = Post.objects.filter(user=following) 
            count = count -1
        elif count < max and count > 0:
            mydata = mydata | Post.objects.filter(user=following) 
            count = count -1
    return render(request, "network/index.html", {
           "posts": mydata,
           "show_new_post": False,
           "title": "Following Posts"
        })

def profile(request, id):
    user = User.objects.get(id=id)
    logged_user = request.user
    return render(request, "network/profile.html", {
           "posts": Post.objects.filter(user=user).order_by('-date_creation'),
           "user": user,
           "month": user.date_creation.strftime("%B"),
           "year":user.date_creation.year,
           "following": user.following.count(),
           "followers": user.followers.count(),
           "login_user": request.user,
           "option": ifFollowing(logged_user, user),
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        date_creation = date.today()
        date_update =  date.today()

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



def new_post (request):
    if request.method == "POST":
        new_post = Post()
        new_post.user = request.user
        new_post.text = request.POST["text"]
        new_post.save()
        return HttpResponseRedirect(reverse("index")) 
        