""" Test the tags API """

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Post
from post.serializers import TagSerializer

TAGS_URL = reverse('post:tag-list')


def detail_url(tag_id):
    """ Return tag detail URL """
    return reverse('post:tag-detail', args=[tag_id])


def create_user(email='create_user_tag_tests', password='password123'):
    """ Helper function to create a user"""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """ Test the publicly available tags API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving tags """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """ Test the authorized user tags API """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ Test retrieving tags """
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        response = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        """ Test that tags returned are for the authenticated user """
        user2 = create_user(email='user22example.com')
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_update_tag(self):
        """ Test updating a tag """
        tag = Tag.objects.create(user=self.user, name='Vegan')
        url = detail_url(tag.id)
        payload = {'name': 'Candy'}

        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """ Test deleting a tag """
        tag = Tag.objects.create(user=self.user, name='Vegan')
        url = detail_url(tag.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)

    def test_filter_tags_assigned_posts(self):
        """ Test filtering tags by those assigned to posts """
        tag1 = Tag.objects.create(user=self.user, name='red')
        tag2 = Tag.objects.create(user=self.user, name='blue')
        post = Post.objects.create(
            user=self.user,
            title='Test Post Title',
            content='Test Post Content',
            description='Test Post Description',
        )
        post.tags.add(tag1)

        response = self.client.get(
            TAGS_URL,
            {'assigned_only': 1}
        )

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    # Test that only one tag is returned when filtering by assigned tags
    def test_filter_tags_unique(self):
        """ Test filtering tags by returns unique items """
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Lunch')
        post1 = Post.objects.create(
            user=self.user,
            title='Test Post Title',
            content='Test Post Content',
            description='Test Post Description',
        )
        post1.tags.add(tag)
        post2 = Post.objects.create(
            user=self.user,
            title='Test Post Title 2',
            content='Test Post Content 2',
            description='Test Post Description 2',
        )
        post2.tags.add(tag)

        response = self.client.get(
            TAGS_URL,
            {'assigned_only': 1}
        )

        self.assertEqual(len(response.data), 1)
