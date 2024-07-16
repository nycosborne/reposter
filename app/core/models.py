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
        return user`


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    reddit = models.BooleanField(default=False)
    linkedin = models.BooleanField(default=False)
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
    POST_STATUS = [
        ('DRAFT', 'Draft'),
        ('IN_REVIEW', 'In Review'),
        ('PUBLISHED', 'Published'),
    ]
    status = models.CharField(
        max_length=10,
        choices=POST_STATUS,
        default='DRAFT',
    )
    image = models.ImageField(null=True, upload_to=post_image_file_path)
    created_at = models.DateTimeField(default=timezone.now)

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


# TODO: might wanted to implement a nosql database option for this
class PostServiceEvents(models.Model):
    """PostServiceEvents model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        'Post',
        related_name='post_service_events',
        on_delete=models.CASCADE
    )
    service = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.service


# User Social Accounts setting
# TODO: rename this table to UserSocialAccountsTokens
class UserSocialAccountsSettings(models.Model):
    """UserSocialAccounts model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    # todo need to rethink about the status field
    access_token = models.TextField(blank=True)
    refresh_token = models.CharField(max_length=255, blank=True)
    scope = models.CharField(max_length=255, blank=True)
    access_token_expires_at = models.DateTimeField(default=timezone.now)
    token_type = models.CharField(max_length=255, blank=True)
    id_token = models.TextField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


# TODO: rename this to SocialAccountsOptions
class SocialAccounts(models.Model):
    """SocialAccounts model."""
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    # updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class LinkedinUserInfo(models.Model):
    """Linkedin User info model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    sub = models.CharField(max_length=255)
    name = models.TextField(blank=True)
    given_name = models.CharField(max_length=255, blank=True)
    family_name = models.CharField(max_length=255, blank=True)
    picture = models.TextField(blank=True)
    locale = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class RedditUserInfo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_employee = models.BooleanField(default=False)
    seen_layout_switch = models.BooleanField(default=False)
    has_visited_new_profile = models.BooleanField(default=False)
    pref_no_profanity = models.BooleanField(default=False)
    has_external_account = models.BooleanField(default=False)
    pref_geopopular = models.CharField(max_length=255, blank=True, null=True)
    seen_redesign_modal = models.BooleanField(default=False)
    pref_show_trending = models.BooleanField(default=False)
    subreddit = models.JSONField(blank=True, null=True)
    pref_show_presence = models.BooleanField(default=False)
    snoovatar_img = models.URLField(max_length=1024, blank=True, null=True)
    snoovatar_size = models.JSONField(blank=True, null=True)
    gold_expiration = models.DateTimeField(blank=True, null=True)
    has_gold_subscription = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    num_friends = models.IntegerField(default=0)
    features = models.JSONField(blank=True, null=True)
    can_edit_name = models.BooleanField(default=False)
    verified = models.BooleanField(default=True)
    pref_autoplay = models.BooleanField(default=False)
    coins = models.IntegerField(default=0)
    has_paypal_subscription = models.BooleanField(default=False)
    has_subscribed_to_premium = models.BooleanField(default=False)
    reddit_id = models.CharField(max_length=255, unique=True)
    has_stripe_subscription = models.BooleanField(default=False)
    can_create_subreddit = models.BooleanField(default=False)
    over_18 = models.BooleanField(default=False)
    is_gold = models.BooleanField(default=False)
    is_mod = models.BooleanField(default=True)
    awarder_karma = models.IntegerField(default=0)
    suspension_expiration_utc = models.DateTimeField(blank=True, null=True)
    has_verified_email = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    pref_video_autoplay = models.BooleanField(default=True)
    has_android_subscription = models.BooleanField(default=False)
    in_redesign_beta = models.BooleanField(default=True)
    icon_img = models.URLField(max_length=1024, blank=True, null=True)
    pref_nightmode = models.BooleanField(default=True)
    awardee_karma = models.IntegerField(default=0)
    hide_from_robots = models.BooleanField(default=False)
    password_set = models.BooleanField(default=True)
    link_karma = models.IntegerField(default=0)
    force_password_reset = models.BooleanField(default=False)
    total_karma = models.IntegerField(default=0)
    seen_give_award_tooltip = models.BooleanField(default=False)
    inbox_count = models.IntegerField(default=0)
    seen_premium_adblock_modal = models.BooleanField(default=False)
    pref_top_karma_subreddits = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
