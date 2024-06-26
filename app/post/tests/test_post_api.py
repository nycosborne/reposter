""" Tests for Post API """
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from core.models import Post, Tag
from post.serializers import PostSerializer, PostDetailSerializer

POST_URL = reverse('post:post-list')


def detail_url(post_id):
    """Return post detail URL"""
    return reverse('post:post-detail', args=[post_id])


def image_upload_url(post_id):
    """Create and return an image upload URL."""
    return reverse('post:post-upload-image', args=[post_id])


def create_post(user, **params):
    """Helper function to create a post"""
    defaults = {
        'title': 'Test Post Title',
        'content': 'Test Post Content',
        'description': 'Test Description',
        'link': 'https://testlink.com',
    }

    defaults.update(params)

    post = Post.objects.create(user=user, **defaults)
    return post


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicPostApiTests(TestCase):
    """Test the publicly available Post API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving posts"""
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTests(TestCase):
    """Test the authorized user Post API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="testUser@example.com",
            password="password123"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_posts(self):
        """Test retrieving posts"""
        create_post(user=self.user)
        create_post(user=self.user)

        response = self.client.get(POST_URL)

        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        # assert that this is not empty
        self.assertTrue(len(response.data) > 0)

    def test_posts_limited_to_user(self):
        """Test that posts returned are for the authenticated user"""
        user2 = create_user(
            email="testUser2@example.com",
            password="password123"
        )

        create_post(user=user2)
        create_post(user=self.user)

        response = self.client.get(POST_URL)
        posts = Post.objects.filter(user=self.user)
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_get_post_detail(self):
        """Test retrieving post detail"""
        post = create_post(user=self.user)
        url = detail_url(post.id)
        response = self.client.get(url)
        serializer = PostDetailSerializer(post)
        self.assertEqual(response.data, serializer.data)

    def test_create_basic_post(self):
        """Test creating a post"""
        payload = {
            'title': 'Test Post Title',
            'content': 'Test Post Content',
            'description': 'Test Description',
            'link': 'https://testlink.com',
        }

        response = self.client.post(POST_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=response.data['id'])
        # Looper over all post and print the title
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(post, key))
        self.assertEqual(post.user, self.user)

    def test_partial_update_post(self):
        """Test updating a post with patch"""
        post = create_post(user=self.user)
        new_title = 'Updated Title'
        payload = {'title': new_title}
        url = detail_url(post.id)
        update = self.client.patch(url, payload)
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, new_title)
        self.assertEqual(post.user, self.user)

    def test_full_update_post(self):
        """Test updating a post with put"""
        post = create_post(user=self.user)
        payload = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'description': 'Updated Description',
            'link': 'https://updatedlink.com',
        }
        url = detail_url(post.id)
        update = self.client.put(url, payload)
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(post, key))
        self.assertEqual(post.user, self.user)

    def test_delete_post(self):
        """Test deleting a post"""
        post = create_post(user=self.user)
        url = detail_url(post.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.filter(id=post.id).count(), 0)

    def test_unauthorized_user_delete_post(self):
        """Test deleting a post unauthorized"""
        user2 = create_user(
            email="testUser2@example.com",
            password="password123",
        )
        post = create_post(user=user2)

        url = detail_url(post.id)
        response_using_setup_client = self.client.delete(url)
        self.assertEqual(
            response_using_setup_client.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_create_post_with_new_tags(self):
        """Test creating a post with new tags"""
        payload = {
            'title': 'Test Post Title with tags',
            'content': 'Test Post Content with tags',
            'description': 'Test Description with tags',
            'link': 'https://testlinkwithtags.com',
            'tags': [{'name': 'tag1'}, {'name': 'tag2'}]
        }
        response = self.client.post(POST_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=response.data['id'])
        tags = post.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn('tag1', tags.values_list('name', flat=True))
        self.assertIn('tag2', tags.values_list('name', flat=True))
        for tag in tags:
            self.assertEqual(tag.user, self.user)

    def test_create_post_with_existing_tags(self):
        """Test creating a post with existing tags"""
        existing_tag = Tag.objects.create(user=self.user, name='existing_tag')

        payload = {
            'title': 'Test Post Title with one old tag and one new tag',
            'content': 'Test Post Content with tags',
            'description': 'Test Description with tags',
            'link': 'https://testlinkwithtags.com',
            'tags': [{'name': 'existing_tag'}, {'name': 'tag2'}]
        }

        response = self.client.post(POST_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        posts = Post.objects.filter(user=self.user)
        self.assertEqual(posts.count(), 1)
        post = posts[0]
        # tags = post.tags.all()
        self.assertEqual(post.tags.count(), 2)
        self.assertIn(existing_tag, post.tags.all())
        for tag in payload['tags']:
            exists = post.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_tag_on_post_update(self):
        """Test creating a tag on update"""
        post = create_post(user=self.user)
        payload = {
            'tags': [{'name': 'new_tag_on_update'}]
        }
        url = detail_url(post.id)
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='new_tag_on_update')
        self.assertIn(new_tag, post.tags.all())

    def test_update_post_assign_tag(self):
        """Test updating a post with existing tags"""
        tag1 = Tag.objects.create(user=self.user, name='tag1')
        post = create_post(user=self.user)
        post.tags.add(tag1)

        tag2 = Tag.objects.create(user=self.user, name='tag2')
        payload = {
            'tags': [{'name': 'tag2'}]
        }
        url = detail_url(post.id)
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(tag2, post.tags.all())
        self.assertNotIn(tag1, post.tags.all())

    def test_clear_post_tags(self):
        """Test clearing all tags from a post"""
        tag1 = Tag.objects.create(user=self.user, name='tag1')
        post = create_post(user=self.user)
        post.tags.add(tag1)

        payload = {'tags': []}
        url = detail_url(post.id)
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.tags.count(), 0)
        self.assertNotIn(tag1, post.tags.all())

    def test_filter_posts_by_tags(self):
        """Test filtering posts by tags"""
        post1 = create_post(user=self.user, title='Post 1')
        post2 = create_post(user=self.user, title='Post 2')
        post3 = create_post(user=self.user, title='Post 3 no tags')

        tag1 = Tag.objects.create(user=self.user, name='tag1')
        tag2 = Tag.objects.create(user=self.user, name='tag2')

        post1.tags.add(tag1)
        post2.tags.add(tag2)

        response = self.client.get(
            POST_URL,
            {'tags': f'{tag1.id},{tag2.id}'}
        )

        serializer1 = PostSerializer(post1)
        serializer2 = PostSerializer(post2)
        serializer3 = PostSerializer(post3)

        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)
        self.assertNotIn(serializer3.data, response.data)


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123',
        )
        self.client.force_authenticate(self.user)
        self.post = create_post(user=self.user)

    def tearDown(self):
        self.post.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a post."""
        url = image_upload_url(self.post.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.post.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        url = image_upload_url(self.post.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
