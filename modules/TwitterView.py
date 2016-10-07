
class TwitterView:
    def __init__(self):
        self.col = 40
    def showTimeline(self, tweets):
        """ tweets : `json` object retrieve from API 
        """
        for i in range(0, len(tweets)):
            tweet = tweets[i]
            print('[{0:2}]'.format(i))
            print( u'{0} @{1} : '.format(tweet['user']['name'], tweet['user']['screen_name']) )
            #print(tweet['text'])
            lines = tweet['text'].split('\n')
            for line in lines:
                for i in range(0,9):
                    print('\t'),
                    if len(line) < self.col * (i+1):
                        print(line[self.col*i:])
                        break
                    else:
                        print(line[self.col*i:self.col*(i+1)])
            print('')

    def showMessages(self, messages):
        for mes in messages:
            print( u'{0} @{1} : '.format(mes['sender']['name'], mes['sender']['screen_name']) )
            print( mes['created_at'] )
            lines = mes['text'].split('\n')
            for line in lines:
                for i in range(0,9):
                    print('\t'),
                    if len(line) < self.col * (i+1):
                        print(line[self.col*i:])
                        break
                    else:
                        print(line[self.col*i:self.col*(i+1)])
            print('')

