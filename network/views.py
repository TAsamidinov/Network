from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User
from .models import Post
from .models import Follow

def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all().order_by("-timestamp")
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
        "is_following": is_following
    })

def folowing(request):
    return render(request, "network/folowing.html")

def follow(self, other):
    if self != other:
        Follow.objects.get_or_create(from_user=self, to_user=other)

def unfollow(self, other):
    Follow.objects.filter(from_user=self, to_user=other).delete()









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
