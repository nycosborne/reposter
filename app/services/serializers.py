"""
Serializers for the api end points of the post
"""

from rest_framework import serializers

from core.models import (SocialAccounts,
                         UserSocialAccountsSettings,
                         LinkedinUserInfo,
                         RedditUserInfo,
                         PostServiceEvents)
from services.linkedinAPI import LinkedInAPI
from services.redditAPI import RedditAPI


class SocialAccountsSerializer(serializers.ModelSerializer):
    """Serializer for social accounts objects"""

    class Meta:
        model = SocialAccounts
        fields = ['id', 'name', 'status']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new social account and return it."""
        return SocialAccounts.objects.create(**validated_data)


class PostServiceEventsSerializer(serializers.ModelSerializer):
    """Serializer for post service events objects"""

    class Meta:
        model = PostServiceEvents
        fields = ['id', 'post_id', 'service', 'status']
        read_only_fields = ['id', 'post_id']

    def create(self, validated_data):
        """Create a new post service event and return it."""
        return PostServiceEvents.objects.create(**validated_data)


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    account_type = serializers.CharField(required=False)

    def save(self):
        auth_user = self.context['request'].user
        request = self.context['request']
        if request.data['account_type'] == 'linkedin':
            linkedin_api = LinkedInAPI(auth_user, request)
            code = self.validated_data['code']
            linkedin_api.get_access_token(code)
        if request.data['account_type'] == 'reddit':
            print("CodeSerializer.reddit")
            reddit_api = RedditAPI(auth_user, request)
            code = self.validated_data['code']
            reddit_api.get_access_token(code)


class UserSocialAccountsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAccountsSettings
        fields = [
            'user',
            'name',
            'access_token',
            'access_token_expires_at',
            'refresh_token',
            'scope',
            'token_type',
            'id_token'
        ]


class LinkedinUserInfoSerializer(serializers.ModelSerializer):
    """Serializer for social accounts LinkedinUserInfoSerializer objects"""

    class Meta:
        model = LinkedinUserInfo
        fields = [
            'user',
            'sub',
            'name',
            'given_name',
            'family_name',
            'picture',
            'locale',
            'email',
            'email_verified'
        ]


class RedditUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditUserInfo
        fields = [
            'user',
            'is_employee',
            'seen_layout_switch',
            'has_visited_new_profile',
            'pref_no_profanity',
            'has_external_account',
            'pref_geopopular',
            'seen_redesign_modal',
            'pref_show_trending',
            'subreddit',
            'pref_show_presence',
            'snoovatar_img',
            'snoovatar_size',
            'gold_expiration',
            'has_gold_subscription',
            'is_sponsor',
            'num_friends',
            'features',
            'can_edit_name',
            'verified',
            'pref_autoplay',
            'coins',
            'has_paypal_subscription',
            'has_subscribed_to_premium',
            'reddit_id',
            'has_stripe_subscription',
            'can_create_subreddit',
            'over_18',
            'is_gold',
            'is_mod',
            'awarder_karma',
            'suspension_expiration_utc',
            'has_verified_email',
            'is_suspended',
            'pref_video_autoplay',
            'has_android_subscription',
            'in_redesign_beta',
            'icon_img',
            'pref_nightmode',
            'awardee_karma',
            'hide_from_robots',
            'password_set',
            'link_karma',
            'force_password_reset',
            'total_karma',
            'seen_give_award_tooltip',
            'inbox_count',
            'seen_premium_adblock_modal',
            'pref_top_karma_subreddits'
        ]
