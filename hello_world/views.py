from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from allauth.account.forms import SignupForm
from .models import Meetup, MeetupSignup


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
            messages.success(request, 'Account created successfully! Please check your email to verify your account.')
            return redirect('hello_world:index')
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


@login_required
def meetups(request):
    """Display available meetups and handle signup"""
    if request.method == 'POST':
        meetup_id = request.POST.get('meetup_id')
        try:
            meetup = Meetup.objects.get(id=meetup_id)
            # Check if already signed up
            if MeetupSignup.objects.filter(user=request.user, meetup=meetup).exists():
                messages.warning(request, f'You are already signed up for {meetup.get_location_display()}!')
            else:
                MeetupSignup.objects.create(user=request.user, meetup=meetup)
                messages.success(request, f'Successfully signed up for {meetup.get_location_display()}!')
        except Meetup.DoesNotExist:
            messages.error(request, 'Meetup not found.')
        return redirect('hello_world:meetups')
    
    meetups_list = Meetup.objects.all()
    user_signups = MeetupSignup.objects.filter(user=request.user).values_list('meetup_id', flat=True)
    
    context = {
        'meetups': meetups_list,
        'user_signups': user_signups,
    }
    return render(request, 'meetups.html', context)