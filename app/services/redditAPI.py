import os
import requests
import requests.auth
from dotenv import load_dotenv

load_dotenv()


def set_default_subreddit(user_info):
    if user_info.get('default_set'):
        default_subreddit = user_info.get('display_name')
        prefix = "u_"
        if default_subreddit.startswith(prefix):
            return default_subreddit[len(prefix):]
        return default_subreddit


class RedditAPI:
    def __init__(self, user, request):
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.reddit_redirect_uri = os.getenv('REDDIT_REDIRECT_URI')
        self.user = user
        # self.access_token = (self.user
        #                      .usersocialaccountssettings_set
        #                      .filter(name='reddit')
        #                      .order_by('-created_at').first().access_token)
        # self.subreddit_user_info = (self.user.
        #                             reddituserinfo_set.order_by('-created_at').
        #                             first().subreddit)

    def post_to_reddit(self, data, post_id):
        # TODO: need to refactor this
        access_token = (self.user.
                        usersocialaccountssettings_set.filter(name='reddit').
                        order_by('-created_at').first().access_token)
        subreddit_user_info = (self.user.
                               reddituserinfo_set.order_by('-created_at').
                               first().subreddit)
        # Checks if the user has a default subreddit set
        subreddit = set_default_subreddit(subreddit_user_info)
        print(f"Posting to Reddit: {data}")
        print(f"Post ID: {post_id}")
        print(f"Access Token: {access_token}")
        print(f"Subreddit: {subreddit}")
        headers = {
            'Authorization': 'bearer ' + access_token,
            'User-Agent': 'reposter/0.0.1 (by u/nycosborne)',
        }

        data = {
            'title': data['title'],
            'text': data['content'],
            # TODO: Need to add the link to the post
            'url': 'reposter.com',
            'sr': subreddit,
            'kind': 'link',
            'spoiler': False,
            'nsfw': False,
            'resubmit': False,
            'sendreplies': False,
            'api_type': "json"
        }

        response = requests.post(
            'https://oauth.reddit.com/api/submit', headers=headers, data=data)

        post = self.user.post_set.get(id=post_id)

        if response.status_code == 200:
            post_data = response.json()
            print("Post submitted to reddit successfully.")
            print(f"Post data: {post_data}")
            post.status = 'PUBLISHED'
            post.save()
            return True
        else:
            # TODO: Add error status for posts that failed to post
            # post.status = 'FAILED_TO_POST'
            # post.save()
            print(f"Failed to post. "
                  f"Status code: {response.status_code},"
                  f" Response: {response.text}")
            self.user.reddit = False

    def _check_if_token_is_valid(self):
        access_token = (self.user.
                        usersocialaccountssettings_set.filter(name='reddit').
                        order_by('-created_at').first().access_token)
        return access_token

    def _get_user_info(self, access_token):
        # TODO: need to refactor this
        from services import serializers as servicesSerializers
        subreddit_user_info = (self.user.
                               reddituserinfo_set.order_by('-created_at').
                               first())

        if subreddit_user_info:
            self.user.reddit = True
            return self.user.reddit

        headers = {
            'Authorization': 'bearer ' + access_token,
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'reposter/0.0.1 (by u/nycosborne)',
        }

        response = requests.get(
            'https://oauth.reddit.com/api/v1/me', headers=headers)

        if response.status_code == 200:
            print("User info obtained successfully.")
            user_info = response.json()
            print(f"User info data!!!!: {user_info}")
            user_info['user'] = self.user.id
            user_info['reddit_id'] = user_info['id']

            serializer = (
                servicesSerializers.RedditUserInfoSerializer(
                    data=user_info))
            if subreddit_user_info:
                self.user.save()
                print("User info data already exists.")
                return self.user.reddit
            if serializer.is_valid():
                self.user.save()
                serializer.save()
                set_default_subreddit(user_info)
                print("User info data saved successfully.")
            else:
                print(f"Failed to save user info data. "
                      f"Errors: {serializer.errors}")
        else:
            print(f"Failed to obtain user info. "
                  f"Status code: {response.status_code},"
                  f" Response: {response.text}")
            self.user.reddit = False
            return self.user.reddit

        return self.user.reddit

    def get_access_token(self, code):
        # TODO: need to refactor this
        from services import serializers as servicesSerializers

        user_social_account_setting = self.user.usersocialaccountssettings_set.filter(name='reddit').order_by(
            '-created_at').first()
        if user_social_account_setting:
            access_token = user_social_account_setting.access_token
            self.user.reddit = True
            print("Access token already exists.")
            return access_token
        else:
            # Handle the case where there is no access token, e.g., by logging, returning an error, or fetching a new token
            print("No access token found for the user.")

        print(f'Getting access token for code: {code}')

        client_auth = requests.auth.HTTPBasicAuth(
            self.reddit_client_id,
            self.reddit_client_secret)

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
                self._get_user_info(access_token_data['access_token'])
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
        return self.user.reddit
