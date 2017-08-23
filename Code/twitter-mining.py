# Sarah M. 2017 
import os
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import string
import sys
import keys
import json
from colors import farben

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            filepath = '/home/pi/Mining-Data/miner-'+ wort +'.json'
            with open(filepath, 'a') as f:
                f.write(data)
                f.write("\n") 
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True
    
def jumpback():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    
if __name__ == '__main__':
    wort = input(farben.AUF + "Bitte wählen Sie eine Zeichenkette, zu der Sie Daten sammeln möchten: " + farben.END)
    jumpback()
                 
    print(farben.AUF + "Daten werden gesammelt..." + farben.END) 
    auth = OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_secret)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=['%s' % wort])
