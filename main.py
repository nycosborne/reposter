import json
import requests.auth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

event = {
    'post_id': '123',
    'img': 'https://www.google.com',
    'excerpt': 'This is a test post',
    'title': 'Test Post'
}

TOKEN_ACCESS_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'


def lambda_handler(event, context):
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

    # Use Reddit's REST API to perform operations
    OAUTH_ENDPOINT = 'https://oauth.reddit.com'
    params_get = {
        'limit': 100
    }
    print(token_id)
    headers_get = {
        'User-Agent': 'Bot by nycosborne',
        'Authorization': 'Bearer ' + token_id
    }

    data = {
        'title': '5 post from Python API',
        'text': 'This is a test post from Python API. Please ignore.',
        'sr': 'nycosborne',  # Replace with the subreddit you want to post to
    }

    response2 = requests.post(OAUTH_ENDPOINT + '/api/submit', headers=headers_get, data=data)
    print(response2.json())

# lambda_handler(event, "")


print(os.getenv('CLIENT_ID'))