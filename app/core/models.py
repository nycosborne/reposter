"""
Database models.
"""
import uuid
import os

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)


def post_image_file_path(instance, filename):
    """Generate file path for new post image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads/post/', filename)


class UserManager(BaseUserManager):
    """User manager."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a new user."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # This will only be call be the command line
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    timezone = models.CharField(max_length=255, default='UTC')

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Post(models.Model):
    """Post model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    image = models.ImageField(null=True, upload_to=post_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
