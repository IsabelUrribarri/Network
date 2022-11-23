from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import date, datetime

from .models import User, Post, UserFollowing


def index(request):
    return render(request, "network/index.html", {
           "posts": Post.objects.all().order_by('-date_creation'),
           "show_new_post": True
        })

def allPosts(request):
    return render(request, "network/index.html", {
           "posts": Post.objects.all().order_by('-date_creation'),
           "show_new_post": False
        })

def profile(request, id):
    user = User.objects.get(id=id)
    return render(request, "network/profile.html", {
           "posts": Post.objects.filter(user=user).order_by('-date_creation'),
           "user": user,
           "month": user.date_creation.strftime("%B"),
           "year":user.date_creation.year,
           "following": 117,
           "followers": 320,
           "login_user": request.user,
           "option": 'Follow',
        })

def followers(request, user_id):
    user = User.objects.get(id=user_id)
    followers = user.followers.all()
    return render(request, "network/followers.html", {
        "user": user,
        "followers": followers
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, date_creation)
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
        