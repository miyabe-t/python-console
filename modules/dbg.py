#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shlex
from TwitterRequester import TwitterRequester, TwitterRequestError

VERSION='0.0.1'

class TwitterCLICommands:
    def __init__(self):
        self.get  = [ 'g', 'get' ]
        self.post = [ 'p', 'post' ]
        self.help = [ 'h', 'help' ]
        self.quit = [ 'q', 'quit', 'exit' ]

class TwitterView:
    def __init__(self):
        pass
    def showTimeline(self, tweets):
        """ tweets : `json` object retrieve from API 
        """
        for tweet in tweets:
            print(tweet)
            print( u'{0} @{1} : '.format(tweet['user']['name'], tweet['user']['screen_name']) )
            print(tweet['text'])
        
class TwitterInteractiveShell:
    def __init__(self):
        self.requester = TwitterRequester()
        self.commands = TwitterCLICommands()
        self.view = TwitterView()
    
    def getHomeTimeline(self):
        try:
            tweets = self.requester.getTweets()
            self.view.showTimeline(tweets)
        except TwitterRequestError as te:
            print(te)

    def get(self, args):
        if len(args) < 2 :
            print('argument error')
            return

        if args[1] == 'home':
            self.getHomeTimeline()
        else :
            print( 'No such a argument can be understood : {0}'.format(args[1]) )

    def post(self, args):
        print(': '),
        text = raw_input()
        self.requester.postTweet(text)
        
    def help(self):
        help = '''
        Usage :
            post = post a tweet
            get  = get timeline which you intend to see
        '''

    def main(self):
        global VERSION
        print("This is CLI twitter client ver.{0}".format(VERSION))

        while True:
            cmd = shlex.split( raw_input('> ') )
            if len(cmd) == 0 : continue
            
            if cmd[0] in self.commands.get:
                self.get(cmd)
            elif cmd[0] in self.commands.post:
                self.post(cmd)
            elif cmd[0] in self.commands.help:
                self.help()
            elif cmd[0] in self.commands.quit:
                return 0
            else :
                print('No such a command : {0}'.format(cmd[0]))

if __name__ == '__main__':
    tc = TwitterInteractiveShell()
    tc.main()
