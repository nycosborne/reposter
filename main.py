import requests.auth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

event = {
    'title': 'Link Test Post',
    'body': 'This is a test post',
    'link': 'https://nycosborne.com/post/un-severed',
}
# Todo: I think body need to me in markdown format

TOKEN_ACCESS_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'


def reddit_post(event, context):
    # Getting Authentication Info
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    headers = {
        'User-Agent': 'Bot by nycosborne',
    }

    # Step 2. Getting Token Access id
    response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)

    if response.status_code == 200:
        token_id = response.json()['access_token']

    headers_post = {
        # 'Content-type': 'application/json',
        'User-Agent': 'reposter by nycosborne',
        'Authorization': 'Bearer ' + token_id
    }

    data = {
        'title': event['title'],
        'text': event['body'],
        'url': event['link'],
        'sr': 'nycosborne',
        'kind': 'link',
        'spoiler': False,
        'nsfw': False,
        'resubmit': False,
        'sendreplies': False,
        'api_type': "json"
    }

    response2 = requests.post('https://oauth.reddit.com/api/submit', headers=headers_post, data=data)
    print(response2.json())


reddit_post(event, "")
