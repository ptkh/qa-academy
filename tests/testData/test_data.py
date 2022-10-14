import json


class TestData:
    href_pattern = r'href=[\'"]?([^\'" >]+)'
    time_format = '%a, %d %b %Y %H:%M:%S %z'
    subscription_confirm_message = 'Your subscription has been successfully confirmed.'

    with open('credentials.json') as f:
        creds = json.load(f)
    email = creds['email']
    refresh_token = creds['refresh_token']
    client_id = creds['client_id']
    client_secret = creds['client_secret']
    gmail_api_url = "https://gmail.googleapis.com"
    token_url = "https://www.googleapis.com/oauth2/v4/token"
