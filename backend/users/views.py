from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db import models
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, CustomPasswordChangeForm
from .models import User

User = get_user_model()


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('projects:list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('projects:list')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view."""
    logout(request)
    return redirect('projects:list')


def user_detail_view(request, user_id):
    """User profile detail view."""
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user-details.html', {'user': user})


@login_required
def edit_profile_view(request, user_id):
    """Edit user profile view."""
    user = get_object_or_404(User, pk=user_id)
    
    # Check if user is editing their own profile or is admin
    if request.user != user and not request.user.is_staff:
        return redirect('users:detail', user_id=user_id)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:detail', user_id=user_id)
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'users/edit_profile.html', {'form': form, 'user': user})


@login_required
def change_password_view(request, user_id):
    """Change password view."""
    user = get_object_or_404(User, pk=user_id)
    
    # Check if user is changing their own password or is admin
    if request.user != user and not request.user.is_staff:
        return redirect('users:detail', user_id=user_id)
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('users:detail', user_id=user_id)
    else:
        form = CustomPasswordChangeForm(user)
    
    return render(request, 'users/change_password.html', {'form': form, 'user': user})


def users_list_view(request):
    """List all users with optional filtering (Variant 1)."""
    participants = User.objects.all().order_by('id')
    active_filter = request.GET.get('filter', '')
    
    if request.user.is_authenticated and active_filter:
        if active_filter == 'favorites_authors':
            # Authors of favorited projects
            favorited_projects = request.user.favorites.all()
            owner_ids = favorited_projects.values_list('owner_id', flat=True).distinct()
            participants = User.objects.filter(id__in=owner_ids)
        elif active_filter == 'my_projects_participants':
            # Participants of my projects
            my_projects = request.user.owned_projects.all()
            participant_ids = my_projects.values_list('participants', flat=True).distinct()
            participants = User.objects.filter(id__in=participant_ids)
        elif active_filter == 'likes_my_projects':
            # Users who like my projects (interested_users)
            my_projects = request.user.owned_projects.all()
            interested_user_ids = my_projects.values_list('interested_users', flat=True).distinct()
            participants = User.objects.filter(id__in=interested_user_ids)
        elif active_filter == 'my_project_members':
            # Members of my projects (participants)
            my_projects = request.user.owned_projects.all()
            participant_ids = my_projects.values_list('participants', flat=True).distinct()
            participants = User.objects.filter(id__in=participant_ids)
    
    context = {
        'participants': participants,
        'active_filter': active_filter,
    }
    
    return render(request, 'users/participants.html', context)


@login_required
def share_profile_view(request, user_id):
    """Share profile link (returns JSON with profile URL)."""
    user = get_object_or_404(User, pk=user_id)
    profile_url = request.build_absolute_uri(f'/users/{user_id}/')
    return JsonResponse({'profile_url': profile_url})
