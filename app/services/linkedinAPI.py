import os
import requests
from dotenv import load_dotenv
from services import serializers as servicesSerializers
from django.contrib.auth import get_user_model

load_dotenv()


class LinkedInAPI:
    def __init__(self, user, request):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.linkedin_redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
        self.user = user
        self.request = request

    # load_dotenv

    def get_access_token(self, code):
        print(f"Getting access token for code: {code}!!! "
              f"user ID: {self.user.id}, "
              f"request: {self.request}")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.linkedin_redirect_uri
        }

        response = requests.post(
            'https://www.linkedin.com/oauth/v2/accessToken',
            headers=headers, data=data
        )

        if response.status_code == 200:
            print(f"Access token obtained successfully.")
            access_token_data = response.json()
            print(f"Response!@#!@#!#: {access_token_data}")
            print(f"User ID121234231424: {self.user.id}")
            access_token_data['user'] = self.user.id
            serializer = servicesSerializers.UserSocialAccountsSettingsSerializer(data=access_token_data)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Failed to save access token data. Errors: {serializer.errors}")
        else:
            print(f"Failed to obtain access token. Status code: {response.status_code}, Response: {response.text}")

# Example usage
# linkedin_api = LinkedInAPI()
# linkedin_api.check_access_token()
# linkedin_api.post_linkedin('Test API')
