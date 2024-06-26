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

    def post_to_linkedin(self, data, post_id):

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
            return False

    def _get_user_info(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(
            'https://api.linkedin.com/v2/userinfo',
            headers=headers
        )
        linkedin_user_info = response.json()
        linkedin_user_info['user'] = self.user.id
        locale = linkedin_user_info['locale']
        linkedin_user_info['locale'] = \
            f"{locale['language']}-{locale['country']}"
        print(f"Linkedin user info: {linkedin_user_info}")
        serializer = (
            servicesSerializers.LinkedinUserInfoSerializer(
                data=linkedin_user_info))
        if serializer.is_valid():
            serializer.save()
        else:
            print(f"Failed to save linkedin user info. "
                  f"Errors: {serializer.errors}")

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
                self.user.linkedin = True
                self.user.save()
                serializer.save()
                print(f"Saved: {access_token_data}")
                self._get_user_info(access_token_data['access_token'])
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
