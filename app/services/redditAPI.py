import os
import requests
import requests.auth
from dotenv import load_dotenv
import base64

load_dotenv()


class RedditAPI:
    def __init__(self, user, request):
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.reddit_redirect_uri = os.getenv('REDDIT_REDIRECT_URI')
        self.user = user
        self.request = request

    def post_to_reddit(self, data, post_id):
        pass

    def get_access_token(self, code):
        # TODO: need to refactor this
        from services import serializers as servicesSerializers
        print(f'Getting access token for code: {code}')
        # credentials = f"{self.reddit_client_id}:{self.reddit_client_secret}"
        # encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        client_auth = requests.auth.HTTPBasicAuth(self.reddit_client_id, self.reddit_client_secret)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'reposter/0.0.1 (by u/nycosborne)',
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.reddit_redirect_uri
        }

        print(f"Headers: {headers}")
        print(f'Client Auth: {client_auth.password}, {client_auth.username}')
        print(f"Data: {data}")
        print(f"reddit_redirect_uri: {self.reddit_redirect_uri}")

        response = requests.post(
            'https://www.reddit.com/api/v1/access_token',
            headers=headers, data=data, auth=client_auth
        )
        print(f"Response: {response}")
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
