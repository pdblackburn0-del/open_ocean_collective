from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from allauth.account.forms import SignupForm
from .models import Meetup, MeetupSignup, Story, Comment


def index(request):
    return render(request, 'index.html')

def meetups(request):
    """Display available surf trips"""
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to sign up.")
            return redirect("account_login")

        trip = request.POST.get("trip")

        # Optional: Save to DB
        # MeetupSignup.objects.create(user=request.user, trip=trip)

        messages.success(request, "You're signed up!")
        return redirect("hello_world:meetups")

    return render(request, 'surftrips.html')


def login(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('hello_world:index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'signin.html')


def signup(request):
    """Handle user registration using allauth"""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, 'Account created successfully! Welcome to Open Ocean Collective!')
            return redirect('hello_world:welcome')
        else:
            # Pass form with errors to template
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})


# Step 5: Member-only page
@login_required
def create_story(request):
    """Handle story creation and posting"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        image_url = request.POST.get('image_url', '')
        
        if title and author and content:
            Story.objects.create(
                title=title,
                author=author,
                content=content,
                image_url=image_url,
                author_user=request.user
            )
            messages.success(request, 'Your story has been posted! Thank you for sharing your journey.')
            return redirect('hello_world:stories')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'create_story.html')


def meetups(request):
    """Display available surf trips"""
    return render(request, 'surftrips.html')

def homepage(request):
    return render(request, "homepage.html")


def welcome(request):
    """Welcome page for newly signed up users"""
    return render(request, 'welcome.html')


def logout_view(request):
    """Custom logout view that shows confirmation then logs out and redirects to homepage"""
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, 'You have been signed out.')
        return redirect('hello_world:homepage')
    
    # Show logout confirmation template
    return render(request, 'account/logout.html')


def stories(request):
    """Display community stories and handle comments"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Redirect unauthenticated users to the login page, then back to stories
            messages.error(request, 'You must be logged in to comment.')
            return redirect(f"/accounts/login/?next={request.path}")
        
        story_type = request.POST.get('story_type')
        comment_text = request.POST.get('comment')
        
        # Handle static story comments (rob_static, maya_static, ahmed_static)
        if story_type and story_type.endswith('_static'):
            if comment_text.strip():
                messages.success(request, 'Thank you for your comment on this story!')
            else:
                messages.warning(request, 'Comment cannot be empty.')
        else:
            # Handle dynamic story comments from database
            story_id = request.POST.get('story_id')
            try:
                story = Story.objects.get(id=story_id)
                if comment_text.strip():
                    Comment.objects.create(
                        story=story,
                        user=request.user,
                        content=comment_text
                    )
                    messages.success(request, 'Your comment has been posted!')
                else:
                    messages.warning(request, 'Comment cannot be empty.')
            except Story.DoesNotExist:
                messages.error(request, 'Story not found.')
        
        return redirect('hello_world:stories')
    
    stories = Story.objects.all()
    context = {
        'stories': stories
    }
    return render(request, 'stories.html', context)


@login_required
def edit_story(request, story_id):
    """Handle story editing"""
    try:
        story = Story.objects.get(id=story_id)
    except Story.DoesNotExist:
        messages.error(request, 'Story not found.')
        return redirect('hello_world:stories')
    
    # Check if user is the author
    if story.author_user != request.user:
        messages.error(request, 'You can only edit your own stories.')
        return redirect('hello_world:stories')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image_url = request.POST.get('image_url', '')
        
        if title and content:
            story.title = title
            story.content = content
            story.image_url = image_url
            story.save()
            messages.success(request, 'Your story has been updated!')
            return redirect('hello_world:stories')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'story': story,
        'is_edit': True
    }
    return render(request, 'edit_story.html', context)


@login_required
def delete_story(request, story_id):
    """Handle story deletion"""
    try:
        story = Story.objects.get(id=story_id)
    except Story.DoesNotExist:
        messages.error(request, 'Story not found.')
        return redirect('hello_world:stories')
    
    # Check if user is the author
    if story.author_user != request.user:
        messages.error(request, 'You can only delete your own stories.')
        return redirect('hello_world:stories')
    
    if request.method == 'POST':
        story_title = story.title
        story.delete()
        messages.success(request, f'Your story "{story_title}" has been deleted.')
        return redirect('hello_world:stories')
    
    # Show confirmation template
    context = {
        'story': story
    }
    return render(request, 'delete_story.html', context)


@login_required
def edit_comment(request, comment_id):
    """Handle comment editing"""
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        messages.error(request, 'Comment not found.')
        return redirect('hello_world:stories')
    
    # Check if user is the author
    if comment.user != request.user:
        messages.error(request, 'You can only edit your own comments.')
        return redirect('hello_world:stories')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        if content.strip():
            comment.content = content
            comment.save()
            messages.success(request, 'Your comment has been updated!')
        else:
            messages.error(request, 'Comment cannot be empty.')
        
        return redirect('hello_world:stories')
    
    context = {
        'comment': comment
    }
    return render(request, 'edit_comment.html', context)


@login_required
def delete_comment(request, comment_id):
    """Handle comment deletion"""
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        messages.error(request, 'Comment not found.')
        return redirect('hello_world:stories')
    
    # Check if user is the author
    if comment.user != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('hello_world:stories')
    
    if request.method == 'POST':
        story_id = comment.story.id
        comment.delete()
        messages.success(request, 'Your comment has been deleted.')
        return redirect('hello_world:stories')
    
    # Show confirmation template
    context = {
        'comment': comment
    }
    return render(request, 'delete_comment.html', context)