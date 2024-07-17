import os
import requests
from dotenv import load_dotenv

load_dotenv()


class LinkedInAPI:
    def __init__(self, user, request):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.linkedin_redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
        self.user = user
        self.request = request
        self.access_token = (self.user.
                             usersocialaccountssettings_set
                             .filter(name='linkedin')
                             .order_by('-created_at').first())
        self.sub = (self.user.
                    linkedinuserinfo_set.order_by('-created_at').
                    first())

    def linkedin_api_request(
            self,
            method,
            endpoint,
            data=None,
            headers=None,
            fresh_token=None
    ):
        query_result = self.user.usersocialaccountssettings_set.filter(
            name='linkedin').order_by('-created_at').first()
        if query_result is None:
            raise ValueError("No LinkedIn access token found for the user.")
        access_token = query_result.access_token

        url = f'https://api.linkedin.com/v2/{endpoint}'

        if fresh_token:
            access_token = fresh_token

        payload = None

        # test post payload
        if endpoint == 'ugcPosts':

            sub_query_result = self.user.linkedinuserinfo_set.order_by(
                '-created_at').first()
            if sub_query_result is None:
                raise ValueError("No LinkedIn user info found for the user.")
            sub = sub_query_result.sub
            payload = {
                "author": f"urn:li:person:{sub}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": f"{data}"
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

        if not headers:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

        response = requests.request(method, url, headers=headers, json=payload)
        return response

    def post_to_linkedin(self, data, post_id):
        response = self.linkedin_api_request(
            'POST', 'ugcPosts', data['content'])

        if response.status_code == 201:
            print("Post shared successfully.")
            post = self.user.post_set.get(id=post_id)
            post.status = 'PUBLISHED'
            post.save()
            return True
        else:
            # TODO: Add error status for posts that failed to post
            # post.status = 'FAILED_TO_POST'
            # post.save()
            print(f"Failed to share post. "
                  f"Status code: {response.status_code},"
                  f" Response: {response.text}")
            return False

    def _get_user_info(self, access_token):
        # TODO: need to refactor this
        # this class should not be rependent on services servicesSerializers
        from services import serializers as servicesSerializers

        response = self.linkedin_api_request(
            'GET', 'userinfo', fresh_token=access_token)

        print(f"Response: {response.text}")

        if response.status_code == 200:
            linkedin_user_info = response.json()
            linkedin_user_info['user'] = self.user.id
            locale = linkedin_user_info['locale']
            linkedin_user_info['locale'] = \
                f"{locale['language']}-{locale['country']}"
            print(f"Linkedin user info: {linkedin_user_info}")
            serializer = (
                servicesSerializers.LinkedinUserInfoSerializer(
                    data=linkedin_user_info))
            if self.sub:
                print("User info data already exists.")
                return self.user.linkedin

            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Failed to save linkedin user info. "
                      f"Errors: {serializer.errors}")
        else:
            print(f"Failed to obtain user info. "
                  f"Status code: {response.status_code},"
                  f" Response: {response.text}")
            self.user.linkedin = False
            return self.user.linkedin

        return self.user.linkedin

    def get_access_token(self, code):
        # TODO: need to refactor this
        from services import serializers as servicesSerializers

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
            print(f"Access token data!!!: {access_token_data}")
            serializer = (
                servicesSerializers.UserSocialAccountsSettingsSerializer(
                    data=access_token_data))

            if serializer.is_valid():
                self.user.linkedin = True
                self.user.save()
                serializer.save()
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
