""" Tests for Models """
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(
        email='testUser_sample_user@example.com',
        password='test123'
):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
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
