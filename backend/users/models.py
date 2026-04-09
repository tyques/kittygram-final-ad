import random
import io
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw, ImageFont


class UserManager(BaseUserManager):
    """Custom user manager that uses email as the username field."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


def generate_avatar(name, surname):
    """Generate an avatar with the first letter of the name on a colored background."""
    # Get the first letter of the name
    first_letter = name[0].upper() if name else 'U'
    
    # Generate a random pastel color for the background
    colors = [
        (173, 216, 230),  # Light blue
        (144, 238, 144),  # Light green
        (255, 182, 193),  # Light pink
        (255, 218, 185),  # Light orange
        (221, 160, 221),  # Light purple
        (176, 224, 230),  # Light cyan
        (255, 228, 181),  # Light yellow
        (216, 191, 216),  # Thistle
        (176, 196, 222),  # Light steel blue
        (152, 251, 152),  # Pale green
    ]
    bg_color = random.choice(colors)
    
    # Create image
    img = Image.new('RGB', (200, 200), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fall back to default if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        except (IOError, OSError):
            font = ImageFont.load_default()
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), first_letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (200 - text_width) // 2
    y = (200 - text_height) // 2
    
    # Draw the letter in dark gray for good contrast
    draw.text((x, y), first_letter, fill=(50, 50, 50), font=font)
    
    # Save to bytes
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return InMemoryUploadedFile(
        img_io,
        'ImageField',
        f'avatar_{name}_{surname}.png',
        'image/png',
        img_io.getbuffer().nbytes,
        None
    )


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for TeamFinder."""
    
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=124, verbose_name='Name')
    surname = models.CharField(max_length=124, verbose_name='Surname')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Avatar')
    phone = models.CharField(max_length=12, unique=True, verbose_name='Phone')
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub URL')
    about = models.TextField(max_length=256, blank=True, verbose_name='About')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    
    # Variant 1: Favorites
    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True,
        verbose_name='Favorites'
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.surname} {self.name}'
    
    def save(self, *args, **kwargs):
        # Generate avatar if not set
        if not self.avatar and self.name:
            self.avatar = generate_avatar(self.name, self.surname)
        super().save(*args, **kwargs)
