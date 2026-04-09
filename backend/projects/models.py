from django.db import models
from django.conf import settings


class Project(models.Model):
    """Model for pet projects in TeamFinder."""
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Project name')
    description = models.TextField(blank=True, verbose_name='Description')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Owner'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub URL')
    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name='Status'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participated_projects',
        blank=True,
        verbose_name='Participants'
    )
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
