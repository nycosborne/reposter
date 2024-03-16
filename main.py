import json
import requests.auth
import os

from markdownify import markdownify as md
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# This is a test post
# event['body'] = {
#     'title': 'Link Test Post',
#     'body': 'This is a test post',
#     'link': 'https://nycosborne.com/post/un-severed',
# }

TOKEN_ACCESS_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'

def reddit_post(event, context):
    print(event['body'])

    if isinstance(event['body'], str):
        event_body = json.loads(event['body'])

    # Getting Authentication Info
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    headers = {
        'User-Agent': 'Bot by nycosborne',
    }

    # Getting Token Access id
    response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)

    if response.status_code == 200:
        token_id = response.json()['access_token']

    headers_post = {
        'User-Agent': 'reposter by nycosborne',
        'Authorization': 'Bearer ' + token_id
    }

    data = {
        'title': event_body['title'],
        'text': md(event_body['body']),
        'url': event_body['link'],
        'sr': 'nycosborne',
        'kind': 'link',
        'spoiler': False,
        'nsfw': False,
        'resubmit': False,
        'sendreplies': False,
        'api_type': "json"
    }

    response2 = requests.post('https://oauth.reddit.com/api/submit', headers=headers_post, data=data)
    print(response2.json()['json']['data']['url'])

    # return url for new post
    return {
        'statusCode': 200,
        'body': json.dumps(response2.json()['json']['data']['url'])
    }
