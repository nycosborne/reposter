""" Tests for Models """
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
from core.models import UserSocialAccountsSettings
from core.models import LinkedinUserInfo


# from services.linkedinAPI import LinkedInAPI


def sample_user(
        email='testUser_sample_user@example.com',
        password='test123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        first_name = 'Test User'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
        )

        # Check if email is equal to the email we passed in
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, expected)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test1@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_post(self):
        """Test creating a new post"""
        user = get_user_model().objects.create_user(
            'testuser@example.com',
            'test123'
        )

        post = models.Post.objects.create(
            user=user,
            title='Test Post Title',
            content='Test Post Content',
            description='Test Post Description',
        )

        self.assertEqual(post.title, 'Test Post Title')
        self.assertEqual(str(post), 'Test Post Title')
        self.assertEqual(post.content, 'Test Post Content')

    def test_create_tag(self):
        """Test creating a new tag"""
        user = sample_user()
        tag = models.Tag.objects.create(
            user=user,
            name='Test Tag'
        )

        self.assertEqual(tag.name, 'Test Tag')

    @patch('core.models.uuid.uuid4')
    def test_post_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.post_image_file_path(None, 'test_image.jpg')

        exp_path = f'uploads/post/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)


class UserSocialAccountsSettingsModelTests(TestCase):
    """Test UserSocialAccountsSettings model"""

    def setUp(self):
        self.user = sample_user()
        self.user_social_account_setting = UserSocialAccountsSettings.objects.create(
            user=self.user,
            name='LinkedIn',
            access_token='ABC123',
            refresh_token='XYZ789',
            scope='r_liteprofile',
            token_type='Bearer'
        )

    def test_user_social_accounts_settings_creation(self):
        """Test creating a UserSocialAccountsSettings is successful"""
        self.assertEqual(self.user_social_account_setting.name, 'LinkedIn')
        self.assertEqual(str(self.user_social_account_setting), 'LinkedIn')
        self.assertEqual(self.user_social_account_setting.access_token, 'ABC123')
        self.assertEqual(self.user_social_account_setting.user, self.user)


class LinkedinUserInfoIModelTests(TestCase):
    """Test LinkedinUserInfo model"""

    def setUp(self):
        self.user = sample_user()
        self.linkedin_user_info = LinkedinUserInfo.objects.create(
            user=self.user,
            sub='ABC123',
            name='XYZ789',
            given_name='Jim',
            family_name='Django',
            picture='nycosborne.com/ny.jpg',
            locale='ID123',
            email='dan@example.com',
            email_verified=False
        )

    def test_linkedin_user_info_creation(self):
        """Test creating a LinkedinUserInfo is successful"""
        self.assertEqual(self.linkedin_user_info.sub, 'ABC123')
        self.assertEqual(str(self.linkedin_user_info), 'XYZ789')
        self.assertEqual(self.linkedin_user_info.given_name, 'Jim')
        self.assertEqual(self.linkedin_user_info.family_name, 'Django')
        self.assertEqual(self.linkedin_user_info.picture, 'nycosborne.com/ny.jpg')
        self.assertEqual(self.linkedin_user_info.locale, 'ID123')
        self.assertEqual(self.linkedin_user_info.email, 'dan@example.com')
