from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from allauth.account.forms import SignupForm
from .models import Meetup, MeetupSignup, Story, Comment


def index(request):
    return render(request, 'index.html')


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
    return render(request, 'create_story.html')


def meetups(request):
    """Display available surf trips"""
    return render(request, 'surftrips.html')

def homepage(request):
    return render(request, "homepage.html")


def welcome(request):
    """Welcome page for newly signed up users"""
    return render(request, 'welcome.html')


def stories(request):
    """Display community stories and handle comments"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('hello_world:stories')
        
        story_id = request.POST.get('story_id')
        comment_text = request.POST.get('comment')
        
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