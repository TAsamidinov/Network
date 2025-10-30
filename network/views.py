from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User
from .models import Post
from .models import Follow

def index(request):
    posts_qs = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts_qs, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })
def newPost(request):
    if request.method == "POST":
        author = request.user
        post_content = request.POST["content"]

        post = Post.objects.create(author=author, content=post_content)
        post.save() 
        
        alert_message = "Post created successfully!"

        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "network/newPost.html")

def profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(from_user=request.user, to_user=User.objects.get(username=username)).exists()

    return render(request, "network/profile.html", {
        "profile_user": User.objects.get(username=username),
        "posts": Post.objects.filter(author=User.objects.get(username=username)).order_by("-timestamp"),
        "is_following": is_following,
        "page_obj": Paginator(Post.objects.filter(author=User.objects.get(username=username)).order_by("-timestamp"), 10).get_page(request.GET.get("page", 1))
    })

def following(request):
        followed_users = Follow.objects.filter(from_user=request.user).values_list("to_user", flat=True)

        # Get posts authored by those followed users
        posts = Post.objects.filter(author__in=followed_users).order_by("-timestamp")

        return render(request, "network/following.html", {
            "posts": posts
        })

def follow(request, username):
    other = get_object_or_404(User, username=username)
    request.user.follow(other)

    return redirect("profile", username=other.username)

def unfollow(request, username):
    other = get_object_or_404(User, username=username)
    request.user.unfollow(other)

    return redirect("profile", username=other.username)

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
