# Generated by Django 5.0.6 on 2024-07-06 22:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_socialaccounts_post_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedditUserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_employee', models.BooleanField(default=False)),
                ('seen_layout_switch', models.BooleanField(default=False)),
                ('has_visited_new_profile', models.BooleanField(default=False)),
                ('pref_no_profanity', models.BooleanField(default=False)),
                ('has_external_account', models.BooleanField(default=False)),
                ('pref_geopopular', models.CharField(blank=True, max_length=255, null=True)),
                ('seen_redesign_modal', models.BooleanField(default=False)),
                ('pref_show_trending', models.BooleanField(default=False)),
                ('subreddit', models.JSONField(blank=True, null=True)),
                ('pref_show_presence', models.BooleanField(default=False)),
                ('snoovatar_img', models.URLField(blank=True, max_length=1024, null=True)),
                ('snoovatar_size', models.JSONField(blank=True, null=True)),
                ('gold_expiration', models.DateTimeField(blank=True, null=True)),
                ('has_gold_subscription', models.BooleanField(default=False)),
                ('is_sponsor', models.BooleanField(default=False)),
                ('num_friends', models.IntegerField(default=0)),
                ('features', models.JSONField(blank=True, null=True)),
                ('can_edit_name', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=True)),
                ('pref_autoplay', models.BooleanField(default=False)),
                ('coins', models.IntegerField(default=0)),
                ('has_paypal_subscription', models.BooleanField(default=False)),
                ('has_subscribed_to_premium', models.BooleanField(default=False)),
                ('reddit_id', models.CharField(max_length=255, unique=True)),
                ('has_stripe_subscription', models.BooleanField(default=False)),
                ('can_create_subreddit', models.BooleanField(default=False)),
                ('over_18', models.BooleanField(default=False)),
                ('is_gold', models.BooleanField(default=False)),
                ('is_mod', models.BooleanField(default=True)),
                ('awarder_karma', models.IntegerField(default=0)),
                ('suspension_expiration_utc', models.DateTimeField(blank=True, null=True)),
                ('has_verified_email', models.BooleanField(default=True)),
                ('is_suspended', models.BooleanField(default=False)),
                ('pref_video_autoplay', models.BooleanField(default=True)),
                ('has_android_subscription', models.BooleanField(default=False)),
                ('in_redesign_beta', models.BooleanField(default=True)),
                ('icon_img', models.URLField(blank=True, max_length=1024, null=True)),
                ('pref_nightmode', models.BooleanField(default=True)),
                ('awardee_karma', models.IntegerField(default=0)),
                ('hide_from_robots', models.BooleanField(default=False)),
                ('password_set', models.BooleanField(default=True)),
                ('link_karma', models.IntegerField(default=0)),
                ('force_password_reset', models.BooleanField(default=False)),
                ('total_karma', models.IntegerField(default=0)),
                ('seen_give_award_tooltip', models.BooleanField(default=False)),
                ('inbox_count', models.IntegerField(default=0)),
                ('seen_premium_adblock_modal', models.BooleanField(default=False)),
                ('pref_top_karma_subreddits', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
