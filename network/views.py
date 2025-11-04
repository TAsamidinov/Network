from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed, Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json

from .models import User, Post, Follow

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

@login_required
@require_http_methods(["PUT"])
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponse(status=403)
    
    try: 
        data = json.loads(request.body.decode("utf-8"))
        content = data.get("content", "").strip()
        if not content:
            return HttpResponse(status=400)
        
        post.content = content
        post.save()
        return JsonResponse({"message": "Post updated successfully.", "content": post.content})
    
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    
@login_required
@require_http_methods(["PUT"])
def edit_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found")

    if post.author != request.user:
        return HttpResponseForbidden("Not allowed")

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    content = (payload.get("content") or "").strip()
    if not content:
        return HttpResponseBadRequest("Content cannot be empty")

    post.content = content
    post.save(update_fields=["content"])
    return JsonResponse({"content": post.content})

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

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post_id.like == request.user:
        post.likes -= 1
    else:
        post.likes += 1
        
    post.save()
    return JsonResponse({"likes": post.likes})

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
