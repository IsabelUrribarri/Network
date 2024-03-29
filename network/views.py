import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import date, datetime
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import User, Post, UserFollowing, Like
from django.views.decorators.csrf import csrf_exempt

def ifFollowing(following, follower):
    result = following.following.filter(following_user_id=follower)
    if result.count() > 0:
        return 'Unfollow'
    else: 
        return 'Follow'

def index(request, post_id=None):
    objects = Post.objects.all().order_by('-date_creation')
    paginator = Paginator(objects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages = []
    if request.user.is_anonymous:
        return render(request, "network/login.html")
    else: 
        posts_con_like = postsConLike(request.user)
        if post_id is not None:
            return render(request, "network/index.html", {
            "posts": page_obj,
            "show_new_post": False,
            "posts_con_like": posts_con_like,
            "post": Post.objects.get(id=post_id)
            })
    return render(request, "network/index.html", {
        "posts": page_obj,
        "show_new_post": True,
        "posts_con_like": posts_con_like
        
        })

@csrf_exempt
def follow_unfollow(request):
    user = request.user
    data = json.loads(request.body)
    following_user_id = data.get('following_user_id')
    following_user = User.objects.get(id=following_user_id)
    if data.get('action') == 'Unfollow':
        UserFollowing.objects.filter(user_id=user, following_user_id=following_user).delete()
        number_of_followers = following_user.followers.count()
        
    elif data.get('action') == 'Follow':
        user_following = UserFollowing()
        user_following.user_id = user
        user_following.following_user_id = following_user
        user_following.save()
        number_of_followers = following_user.followers.count()
    return JsonResponse({
        "message": f"El usuario {following_user.username} fue seguido", 
        "number_of_followers": number_of_followers
        },
         status=201)

def get_post(request, post_id):
    post = Post.objects.get(id=post_id)
    return JsonResponse({
        "text": post.text
        }, status=201)

def set_like(request, post_id):
    post = Post.objects.get(id=post_id)
    like = Like.objects.filter(post=post, user=request.user).count()
    #si no le ha dado like, asociar el like
    print(like)
    if like == 0:
        new_like = Like()
        new_like.post = post
        new_like.user = request.user
        new_like.save()
        msg = 'Like'
    #si tenia like se lo quito
    else:
        Like.objects.filter(post=post, user=request.user).delete()
        msg = 'Dislike'
    return JsonResponse({
        "text": msg
        }, status=201)

def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    like = Like.objects.filter(post=post, user=request.user).count()
    #si no le ha dado like, asociar el like
    print(like)
    if like == 0:
        new_like = Like()
        new_like.post = post
        new_like.user = request.user
        new_like.save()
        msg = 'Like'
    #si tenia like se lo quito
    else:
        Like.objects.filter(post=post, user=request.user).delete()
        msg = 'Dislike'
    return JsonResponse({
        "text": msg,
        "like_count": post.post_likes.count() 
        }, status=201)

def allPosts(request):
    objects = Post.objects.all().order_by('-date_creation')
    paginator = Paginator(objects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages = []
    if request.user.is_anonymous:
        return render(request, "network/login.html")
    posts_con_like = postsConLike(request.user)      
    return render(request, "network/index.html", {
        "posts": page_obj,
        "show_new_post": False,
        "title": "All Posts",
        "posts_con_like": posts_con_like
        })


def followingPosts(request, id):
    if request.user.is_anonymous:
        return render(request, "network/login.html")
    user = User.objects.get(id=id)
    max = UserFollowing.objects.filter(user_id=user).count()
    count = max
    mydata = None
    records = UserFollowing.objects.filter(user_id=id)
    for following in records:
        if count == max:
            mydata = Post.objects.filter(user=following.following_user_id) 
            count = count -1
        elif count < max and count > 0:
            mydata = mydata | Post.objects.filter(user=following.following_user_id) 
            count = count -1
    posts_con_like = postsConLike(request.user) 
    return render(request, "network/index.html", {
        "posts": None if mydata is None else mydata.order_by('-date_creation'),
        "show_new_post": False,
        "title": "Following Posts",
        "posts_con_like": posts_con_like
        })

def profile(request, id):
    user = User.objects.get(id=id)
    logged_user = request.user
    posts_con_like = postsConLike(request.user)
    return render(request, "network/profile.html", {
           "posts": Post.objects.filter(user=user).order_by('-date_creation'),
           "user": user,
           "month": user.date_creation.strftime("%B"),
           "year":user.date_creation.year,
           "following": user.following.count(),
           "followers": user.followers.count(),
           "posts_con_like": posts_con_like,
           "login_user": request.user,
           "option": ifFollowing(logged_user, user),
        })

@csrf_exempt
def photo(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        data = json.loads(request.body)
        user.photo_url_image = data["url_photo"]
        user.save()
        return JsonResponse({
            "text": 'url guardados',
            }, status=201)
    else:
        return JsonResponse({
            "text": 'no es un post',
            "url_photo": user.photo_url_image,
            }, status=201)

@csrf_exempt
def banner(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        data = json.loads(request.body)
        user.banner_url_image = data["url_banner"]
        user.save()
        return JsonResponse({
            "text": 'url guardados',
            }, status=201)
    else:
        return JsonResponse({
            "text": 'no es un post',
            "url_banner": user.banner_url_image,
            }, status=201)

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
    
def update_post (request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        post.text = request.POST["text"]
        post.save()
        return HttpResponseRedirect(reverse("index")) 
    else:
        return HttpResponseRedirect(reverse("index")) 

def postsConLike (user):
    # construir lista de post id que tienen like
    # construir lista de likes 
    mis_likes = Like.objects.filter(user=user)
    # recorrer cada like y guardar en una nueva lista los post id
    posts_con_like = []
    for like in mis_likes:
        posts_con_like.append(like.post.id)
    return posts_con_like