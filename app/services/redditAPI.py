import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()


class RedditAPI:
    def __init__(self, user, request):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.linkedin_redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
        self.user = user
        self.request = request

    def post_to_reddit(self, data, post_id):

        access_token = (self.user.
                        usersocialaccountssettings_set.order_by('-created_at').
                        first().access_token)

        sub = (self.user.
               linkedinuserinfo_set.order_by('-created_at').
               first().sub)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payload = {
            "author": f"urn:li:person:{sub}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": f"{data['content']}"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            headers=headers, json=payload
        )

        if response.status_code == 201:
            print("Post shared successfully.")
            post = self.user.post_set.get(id=post_id)
            post.status = 'PUBLISHED'
            post.save()
            return True
        else:
            print(f"Failed to share post. "
                  f"Status code: {response.status_code},"
                  f" Response: {response.text}")

    def get_access_token(self, code):
        # TODO: need to refactor this
        from services import serializers as servicesSerializers
        print(f'Getting access token for code: {code}')
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            # "Content-Type": "application/x-www-form-urlencoded",
            # 'User-Agent': YOUR_USER_AGENT,
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.linkedin_redirect_uri
        }

        print(f"Headers: {headers}")
        print(f"Data: {data}")

        response = requests.post(
            'https://www.linkedin.com/oauth/v2/accessToken',
            headers=headers, data=data
        )

        if response.status_code == 200:
            print("Access token obtained successfully.")
            access_token_data = response.json()
            access_token_data['user'] = self.user.id
            access_token_data['name'] = 'reddit'
            print(f"Got Access token data!!!!: {access_token_data}")
            serializer = (
                servicesSerializers.UserSocialAccountsSettingsSerializer(
                    data=access_token_data))

            if serializer.is_valid():
                self.user.reddit = True
                self.user.save()
                serializer.save()
                print("Access token data saved successfully.")
                # self._get_user_info(access_token_data['access_token'])
            else:
                print(f"Failed to save access token data. "
                      f"Errors: {serializer.errors}")
                self.user.reddit = False
        else:
            print(f"Failed to obtain access token. "
                  f"Status code: {response.status_code},"
                  f" Response: {response.text}")
            self.user.reddit = False
        # Update user social account status
        self.user.save()

    # def get_
