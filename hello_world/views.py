from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from allauth.account.forms import SignupForm

from .models import MeetupSignup, Story, Comment


# =========================
# Public Pages
# =========================

def index(request):
    return render(request, "index.html")


def homepage(request):
    return render(request, "homepage.html")


def welcome(request):
    """Welcome page after signup"""
    return render(request, "welcome.html")


# =========================
# Authentication
# =========================

def login(request):
    """User login"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("hello_world:index")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "account/login.html")


def signup(request):
    """User registration (django-allauth)"""
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save(request)
            messages.success(request, "Account created successfully!")
            return redirect("hello_world:welcome")

        return render(request, "signup.html", {"form": form})

    form = SignupForm()
    return render(request, "account/signup.html", {"form": form})


def logout_view(request):
    """Logout with confirmation page"""
    if request.method == "POST":
        auth_logout(request)
        messages.success(request, "You have been signed out.")
        return redirect("hello_world:homepage")

    return render(request, "account/logout.html")


# =========================
# Meetups / Surf Trips
# =========================

def meetups(request):
    """View + signup for surf trips"""

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to sign up.")
            return redirect("account_login")

        trip = request.POST.get("trip")

        # Optional DB save (if needed)
        # MeetupSignup.objects.create(user=request.user, trip=trip)

        messages.success(request, "You're signed up!")
        return redirect("hello_world:meetups")

    return render(request, "surftrips.html")


# =========================
# Stories
# =========================

def stories(request):
    """View stories + handle comments"""

    if request.method == "POST":

        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect(f"/accounts/login/?next={request.path}")

        story_type = request.POST.get("story_type")
        comment_text = request.POST.get("comment", "")

        # Static story comments (no DB)
        if story_type and story_type.endswith("_static"):
            if comment_text.strip():
                messages.success(request, "Thanks for your comment!")
            else:
                messages.warning(request, "Comment cannot be empty.")
            return redirect("hello_world:stories")

        # Dynamic story comments (DB-backed)
        story_id = request.POST.get("story_id")

        story = get_object_or_404(Story, id=story_id)

        if comment_text.strip():
            Comment.objects.create(
                story=story,
                user=request.user,
                content=comment_text
            )
            messages.success(request, "Your comment has been posted!")
        else:
            messages.warning(request, "Comment cannot be empty.")

        return redirect("hello_world:stories")

    stories = Story.objects.all()
    return render(request, "stories.html", {"stories": stories})


# =========================
# Story CRUD
# =========================

@login_required
def create_story(request):
    """Create a new story"""

    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        content = request.POST.get("content")
        image_url = request.POST.get("image_url", "")

        if title and author and content:
            Story.objects.create(
                title=title,
                author=author,
                content=content,
                image_url=image_url,
                author_user=request.user
            )
            messages.success(request, "Story created successfully!")
            return redirect("hello_world:stories")

        messages.error(request, "Please fill in all required fields.")

    return render(request, "create_story.html")


@login_required
def edit_story(request, story_id):
    """Edit story"""

    story = get_object_or_404(Story, id=story_id)

    if story.author_user != request.user:
        messages.error(request, "You can only edit your own stories.")
        return redirect("hello_world:stories")

    if request.method == "POST":
        story.title = request.POST.get("title")
        story.content = request.POST.get("content")
        story.image_url = request.POST.get("image_url", "")
        story.save()

        messages.success(request, "Story updated!")
        return redirect("hello_world:stories")

    return render(request, "edit_story.html", {"story": story, "is_edit": True})


@login_required
def delete_story(request, story_id):
    """Delete story"""

    story = get_object_or_404(Story, id=story_id)

    if story.author_user != request.user:
        messages.error(request, "You can only delete your own stories.")
        return redirect("hello_world:stories")

    if request.method == "POST":
        story_title = story.title
        story.delete()
        messages.success(request, f'Story "{story_title}" deleted.')
        return redirect("hello_world:stories")

    return render(request, "delete_story.html", {"story": story})


# =========================
# Comment CRUD
# =========================

@login_required
def edit_comment(request, comment_id):
    """Edit comment"""

    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        messages.error(request, "You can only edit your own comments.")
        return redirect("hello_world:stories")

    if request.method == "POST":
        content = request.POST.get("content", "")

        if content.strip():
            comment.content = content
            comment.save()
            messages.success(request, "Comment updated!")
        else:
            messages.error(request, "Comment cannot be empty.")

        return redirect("hello_world:stories")

    return render(request, "edit_comment.html", {"comment": comment})


@login_required
def delete_comment(request, comment_id):
    """Delete comment"""

    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        messages.error(request, "You can only delete your own comments.")
        return redirect("hello_world:stories")

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect("hello_world:stories")

    return render(request, "delete_comment.html", {"comment": comment})