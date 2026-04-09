from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('name', 'description', 'owner', 'github_url', 'status')}),
        ('Participants', {'fields': ('participants',)}),
    )
    
    filter_horizontal = ('participants',)
    
    search_fields = ('name', 'description', 'owner__email', 'owner__name', 'owner__surname')
