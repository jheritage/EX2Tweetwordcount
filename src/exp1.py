"""

"""
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy, copy
from time import time,ctime
import simplejson
import Queue, threading
from streamparse.spout import Spout


consumer_key = "IgcSZd675nvisCYIYOXt9Rfnz";
consumer_secret = "R1D1quBUooIGUDoBtaIkKnfFdI4AUaOloME4y72DU4YNmwvCTV";
access_token = "4050176059-Dk4YFqIxc5ojG3bvBLsqIeNI36gqqVaWFhXZJHl";
access_token_secret = "NlYxAbWyMbSIVsuDpFwJSFxzUeTTKdIAYkGnXuv6v7ou1";

twitter_credentials = {   
    "consumer_key"        :  consumer_key,
    "consumer_secret"     :  consumer_secret,
    "access_token"        :  access_token,
    "access_token_secret" :  access_token_secret,
}


def auth_get(auth_key):
    if auth_key in twitter_credentials:
        return twitter_credentials[auth_key]
    return None



class TweetListener(StreamListener):
   
    def __init__(self,timer):
	StreamListener.__init__(self)
        self.q = Queue.Queue(maxsize=100)

    def on_data(self, data):
        try:
		self.dataJson =simplejson.loads(data[:-1])
                self.dataJsonText = self.dataJson["text"].lower()
                #print 'TestPrint:  ' + self.dataJsonText
		self.q.put(self.dataJsonText)
		return True

        except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status):
        print ("ERROR :",status)



class Tweets(Spout):

    def initialize(self, stormconf, context):
        #self._queue = Queue.Queue(maxsize = 100)
	self.verbose = True

        if auth_get("access_token") and auth_get("access_token_secret"):
            access_token = auth_get("access_token")
            access_token_secret = auth_get("access_token_secret")
            auth.set_access_token(access_token, access_token_secret)

        self._tweepy_api = tweepy.API(auth)

        # Create the listener for twitter stream
        self.listener = TweetListener()

        # Create the stream and listen for english tweets
        stream = tweepy.Stream(auth, self.listener, timeout=None)
        stream.filter(languages=["en"], track=["a", "the", "i", "you", "u"], async=True)

    def queue(self):
        return self.listener.q

    def tweepy_api(self):
        return self._tweepy_api

    def next_tuple(self):
        try:
            tweet = self.queue().get(timeout = 0.1)
            print("T: " +tweet)
            if tweet:
                self.queue().task_done()
                self.emit([tweet])

        except Queue.Empty:
            self.log("Empty queue exception ")
            time.sleep(0.1)
