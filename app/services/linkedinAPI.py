from datetime import datetime, timezone
import os

import requests
from core.models import UserSocialAccountsSettings


class LinkedInAPI:
    def __init__(self, access_token=None):
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')

    def post_linkedin(self, message):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
            'LinkedIn-Version': '202305',
        }

        payload = {
            "author": "urn:li:person:SmvZ3iW1Ma",
            "commentary": message,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }

        response = requests.post('https://api.linkedin.com/v2/posts', headers=headers, json=payload)

        if response.status_code == 201:
            print("Posted successfully on LinkedIn!")
        else:
            print(f"Failed to post on LinkedIn. Status code: {response.status_code}, Response: {response.text}")

    def check_access_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'token': self.access_token
        }

        response = requests.post('https://www.linkedin.com/oauth/v2/introspectToken', headers=headers, data=data)
        expires_at_utc_in_seconds = response.json()['expires_at']
        now_utc_in_seconds = int(datetime.now(timezone.utc).timestamp())

        # If the token is about to expire in 5 days, get a new access token
        if expires_at_utc_in_seconds - now_utc_in_seconds < 432000:
            self.get_access_token()

    def get_access_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'grant_type': 'authorization_code',
            'code': 'YOUR_CODE',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': 'YOUR_REDIRECT'
        }

        response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', headers=headers, data=data)
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            print("Access token obtained successfully.")
        else:
            print(f"Failed to obtain access token. Status code: {response.status_code}, Response: {response.text}")

    def request_code(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': 'YOUR_REDIRECT',
            'state': 'YOUR_STATE',
            'scope': 'YOUR_SCOPE'
        }

        response = requests.get('https://www.linkedin.com/oauth/v2/authorization', headers=headers, data=data)
        if response.status_code == 200:
            print("Authorization code requested successfully.")
        else:
            print(
                f"Failed to request authorization code. Status code: {response.status_code}, Response: {response.text}")

# Example usage
# linkedin_api = LinkedInAPI()
# linkedin_api.check_access_token()
# linkedin_api.post_linkedin('Test API')
