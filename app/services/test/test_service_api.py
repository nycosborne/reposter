# """ Tests for Service API """
# from django.urls import reverse
# from django.test import TestCase
#
# from rest_framework import status
# from rest_framework.test import APIClient
#
# from django.contrib.auth import get_user_model
# from core.models import SocialAccounts
# from core.models import UserSocialAccountsSettings
# from services.linkedinAPI import LinkedInAPI
#
# SERVICE_URL = reverse('services:services-list')
#
#
# def create_user(**params):
#     linkedin_api = LinkedInAPI()
#     linkedin_api.check_access_token()
#     linkedin_api.post_linkedin('Test API')
#     return get_user_model().objects.create_user(**params)
#
#
# def create_service(**params):
#     defaults = {
#         'name': 'Facebook',
#         'status': True,
#     }
#
#     defaults.update(params)
#
#     return SocialAccounts.objects.create(**defaults)
#
#
# def detail_url(service_id):
#     """Return service detail URL"""
#     return reverse('service:service_id-detail', args=[service_id])
#
#
# class PublicServiceApiTests(TestCase):
#     """Test the publicly available service API"""
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_login_required(self):
#         """Test that login is required for retrieving service"""
#         res = self.client.post(SERVICE_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_open_access_to_list_services(self):
#         """Test that login is required for retrieving service"""
#         res = self.client.get(SERVICE_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#
# class PrivateServiceApiTests(TestCase):
#     """Test the authorized user service API"""
#
#     def setUp(self):
#         self.client = APIClient()
#         self.user = create_user(
#             email="testUser@example.com",
#             password="password123"
#         )
#
#         self.client.force_authenticate(self.user)
#
#     def test_retrieve_services(self):
#         """Test retrieving services"""
#         create_service(name='FB', status=True)
#         create_service(name='reddit', status=True)
#
#         res = self.client.get(SERVICE_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(res.data), 2)
#
# # class LinkedAPI(TestCase):
# #     """Test the LinkedIn API"""
#
#     # def setUp(self):
