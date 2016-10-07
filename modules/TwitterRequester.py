#!/usr/bin/python
# coding : utf-8

from requests_oauthlib import OAuth1Session
import json

class TwitterRequestError (Exception):
    def __init__(self, status):
        self.status = 0
        
    def __str__(self):
        print("Request Error : code = {0}".format(self.status) )

class TwitterRequester:
    def __init__(self):
        self.cs_key = 'CnySl2l8xsbzbcz15jGnluX4V'
        self.cs_sec = 'PkuZWF3TjFQtz3bWsHAxSi2mvTFtHZuo7fN9RhcQIA9IuCzZcP'
        self.ac_tok = '777522730648285186-K4IpB7nDLRDrh8Xl3KGQur9WeohdV5Z'
        self.ac_sec = 'TofIHgc8YRoWL1TFCmUHDUQqSPd9pMu4Yz5fzf1JrnJxZ'
        
        self.url_update = "https://api.twitter.com/1.1/statuses/update.json"
        self.url_home_timeline = "https://api.twitter.com/1.1/statuses/home_timeline.json"
        self.url_direct_messages = 'https://api.twitter.com/1.1/direct_messages.json'
        self.url_direct_messages_destroy = 'https://api.twitter.com/1.1/direct_messages/destroy.json'

        self.twitter = OAuth1Session(self.cs_key, self.cs_sec, self.ac_tok, self.ac_sec)
        
    def postTweet(self, body):
        params = {"status": body}
        req = self.twitter.post(self.url_update, params = params)
        
        if req.status_code == 200:
            return 0
        else:
            raise TwitterRequestError(req.status_code)

    def postReply(self, body, target):
        params = {'status' : body, 'in_reply_to_status_id' : target }
        req = self.twitter.post(self.url_update, params=params)

        if req.status_code == 200:
            return 0
        else:
            raise TwitterRequestError(req.status_code)
        
    def getTweets(self, count=10):
        params = {'count':count}
        req = self.twitter.get(self.url_home_timeline, params=params)
        if req.status_code == 200:
            timeline = json.loads(req.text)
            return timeline
        else:
            raise TwitterRequestError(req.status_code)

    def getDirectMessages(self):
        params = {}
        req = self.twitter.get(self.url_direct_messages, params=params)
        if req.status_code == 200:
            timeline = json.loads(req.text)
            return timeline
        else:
            raise TwitterRequestError(req.status_code)

    def destroyDirectMessages(self, id):
        params = { 'id' : id }
        req = self.twitter.post(self.url_direct_messages_destroy, params=params)
        if req.status_code == 200:
            timeline = json.loads(req.text)
            return timeline
        else:
            raise TwitterRequestError(req.status_code)
        
