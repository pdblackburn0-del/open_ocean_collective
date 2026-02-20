from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.forms import SignupForm


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


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