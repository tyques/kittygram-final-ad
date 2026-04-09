from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Status')
    
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
    
    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')
        if github_url:
            # Validate that it's a GitHub URL
            if 'github.com' not in github_url:
                raise forms.ValidationError('URL must be a valid GitHub URL')
        return github_url
