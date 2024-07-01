import os
import requests
from dotenv import load_dotenv
from services import serializers as servicesSerializers

load_dotenv()


class LinkedInAPI:
    def __init__(self, user, request):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.linkedin_redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
        # TODO Should be able to get the user from the request
        self.user = user
        self.request = request

    # load_dotenv

    def post_to_linkedin(self, data):
        access_token = self.user.social_accounts_settings.get(name='linkedin').access_token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payload = {
            "author": "urn:li:person:SmvZ3iW1Ma",
            "commentary": data['content'],
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }

        response = requests.post(
            'https://api.linkedin.com/v2/shares',
            headers=headers, json=data
        )

        if response.status_code == 201:
            print("Post shared successfully.")
        else:
            print(f"Failed to share post. "
                  f"Status code: {response.status_code},"
                  f" Response: {response.text}")

    def get_access_token(self, code):

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
            print("Access token obtained successfully.")
            access_token_data = response.json()
            access_token_data['user'] = self.user.id
            access_token_data['name'] = 'linkedin'
            serializer = (
                servicesSerializers.UserSocialAccountsSettingsSerializer(
                    data=access_token_data))

            if serializer.is_valid():
                serializer.save()
                self.user.linkedin = True
            else:
                print(f"Failed to save access token data. "
                      f"Errors: {serializer.errors}")
                self.user.linkedin = False
        else:
            print(f"Failed to obtain access token. "
                  f"Status code: {response.status_code},"
                  f" Response: {response.text}")
            self.user.linkedin = False
        # Update user social account status
        self.user.save()

# Example usage
# linkedin_api = LinkedInAPI()
# linkedin_api.check_access_token()
# linkedin_api.post_linkedin('Test API')
