from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from .models import Project
from .forms import ProjectForm


def project_list_view(request):
    """List all projects with pagination."""
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def favorite_projects_view(request):
    """List user's favorite projects (Variant 1)."""
    projects = request.user.favorites.all().order_by('-created_at')
    return render(request, 'projects/favorite_projects.html', {'projects': projects})


def project_detail_view(request, project_id):
    """Project detail view."""
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def create_project_view(request):
    """Create a new project."""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect('projects:detail', project_id=project.id)
    else:
        form = ProjectForm()
    
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project_view(request, project_id):
    """Edit an existing project."""
    project = get_object_or_404(Project, pk=project_id)
    
    # Check if user is owner or admin
    if request.user != project.owner and not request.user.is_staff:
        return redirect('projects:detail', project_id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


@login_required
@require_POST
def complete_project_view(request, project_id):
    """Complete/close a project (owner only)."""
    project = get_object_or_404(Project, pk=project_id)
    
    # Check if user is owner or admin
    if request.user != project.owner and not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    if project.status == 'open':
        project.status = 'closed'
        project.save()
        return JsonResponse({'status': 'ok', 'project_status': 'closed'})
    
    return JsonResponse({'status': 'error', 'message': 'Project is already closed'}, status=400)


@login_required
@require_POST
def toggle_participate_view(request, project_id):
    """Toggle participation in a project."""
    project = get_object_or_404(Project, pk=project_id)
    
    if request.user in project.participants.all():
        project.participants.remove(request.user)
        is_participating = False
    else:
        project.participants.add(request.user)
        is_participating = True
    
    return JsonResponse({
        'status': 'ok',
        'is_participating': is_participating
    })


@login_required
@require_POST
def toggle_favorite_view(request, project_id):
    """Toggle favorite status for a project (Variant 1)."""
    project = get_object_or_404(Project, pk=project_id)
    
    if request.user in project.interested_users.all():
        project.interested_users.remove(request.user)
        is_favorited = False
    else:
        project.interested_users.add(request.user)
        is_favorited = True
    
    return JsonResponse({
        'status': 'ok',
        'favorited': is_favorited
    })


@login_required
@require_POST
def share_project_view(request, project_id):
    """Share project link (returns JSON with project URL)."""
    project = get_object_or_404(Project, pk=project_id)
    project_url = request.build_absolute_uri(f'/projects/{project_id}/')
    return JsonResponse({'project_url': project_url})
