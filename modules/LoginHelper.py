import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

class UserData:
    def __init__(self):
        self.access_token = ''
        self.access_token_secret = ''

class AppData:
    def __init__(self):
        self.client_key = 'CnySl2l8xsbzbcz15jGnluX4V'
        self.client_secret = 'PkuZWF3TjFQtz3bWsHAxSi2mvTFtHZuo7fN9RhcQIA9IuCzZcP'
        self.url = {
            'oauth_request_token' : 'https://api.twitter.com/oauth/request_token',
            'oauth_authorize' : 'https://api.twitter.com/oauth/authorize',
            'oauth_access_token' : 'https://api.twitter.com/oauth/access_token'
        }

class LoginHelper:
    def __init__(self):
        self.appdata = AppData()

    def main(self):
        oauth = OAuth1(self.appdata.client_key, client_secret=self.appdata.client_secret)
        r = requests.post(url=self.appdata.url['oauth_request_token'], auth=oauth)

        credentials = parse_qs(r.content)
        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]
        authorize_url = self.appdata.url['oauth_authorize'] + '?oauth_token='
        authorize_url = authorize_url + resource_owner_key
        print('Please go ahead to URL with your twitter account logged on.')
        print(authorize_url)
        verifier = raw_input('Please input the verifier : ')#
        
        oauth = OAuth1(self.appdata.client_key,
                       client_secret=self.appdata.client_secret,
                       resource_owner_key=resource_owner_key,
                       resource_owner_secret=resource_owner_secret,
                       verifier=verifier)
        r = requests.post(url=self.appdata.url['oauth_access_token'], auth=oauth)
        credentials = parse_qs(r.content)
        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]
        print('Varification succeed.')
        return (resource_owner_key, resource_owner_secret)

l = LoginHelper()
l.main()
