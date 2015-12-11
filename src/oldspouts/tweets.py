from __future__ import absolute_import, print_function, unicode_literals

import itertools, time
import tweepy, copy 
import Queue, threading
import simplejson
from streamparse.spout import Spout

################################################################################
# Twitter credentials
################################################################################
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


################################################################################
# Class to listen and act on the incoming tweets
################################################################################
class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, listener):
        self.listener = listener
        super(self.__class__, self).__init__(listener.tweepy_api())
	#listener.__init__(self)

    def on_status(self, status):
        self.listener.queue().put(status.text, timeout = 0.01)
        return True
  
    def on_error(self, status_code):
        return True # keep stream alive
  
    def on_limit(self, track):
        return True # keep stream alive

    def on_data(self,data):
	try:
		dataJson = simplejson.loads(data[:-1])
        	dataJsonText = dataJson["text"].lower()
		print(dataJsonText)
		self.listener.queue().put(dataJsonText, timeout = 0.01)
 	
	except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            #pass
	    print("Can't load queue")

class Tweets(Spout):

    def initialize(self, stormconf, context):
        self._queue = Queue.Queue(maxsize = 100)

        consumer_key = auth_get("consumer_key") 
        consumer_secret = auth_get("consumer_secret") 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        if auth_get("access_token") and auth_get("access_token_secret"):
            access_token = auth_get("access_token")
            access_token_secret = auth_get("access_token_secret")
            auth.set_access_token(access_token, access_token_secret)

        self._tweepy_api = tweepy.API(auth)

        # Create the listener for twitter stream
        self.listener = TweetStreamListener(self)

        # Create the stream and listen for english tweets
        stream = tweepy.Stream(auth,self.listener, timeout=None)
        stream.filter(languages=["en"], track=["a", "the", "i", "you", "u"], async=True)

    def queue(self):
        return self._queue

    def tweepy_api(self):
        return self._tweepy_api

    def next_tuple(self):
        #tweet = self.queue().get(timeout = 0.1)
	try:
            tweet = self.queue().get(timeout = 0.1) 
            print("T: " +tweet)
	    if tweet:
                self.queue().task_done()
                self.emit([tweet])
 
        except Queue.Empty:
            self.log("Empty queue exception ")
            time.sleep(0.1) 

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing
