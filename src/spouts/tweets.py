from __future__ import absolute_import, print_function, unicode_literals

import itertools, time
import tweepy, copy 
import Queue, threading
import simplejson
from streamparse.spout import Spout

################################################################################
# Twitter credentials
################################################################################

# Put your twitter credentials here

consumer_key = "" 
consumer_secret = "" 
access_token = ""
access_token_secret = ""

consumer_key = "VHzBSjyzQje6x38wdn5nyoKPE"
consumer_secret = "P6ORjyPH6770GTi01iT3i273VlWIqfSkAVoN33Qj0zJ2JSk14y"
access_token = "4050176059-qc8Qa2CQ92A6e9ex99mIkyxVNvKSIyIkf9atJhP"
access_token_secret = "AHAmoWrba2DMSygc3XZEdxBPndE8I5mgqDP5Vkgvij0TW"


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

    def __init__(self, spout):
        self.spout = spout
        super(self.__class__, self).__init__(spout.tweepy_api())
	#listener.__init__(self)

    def on_status(self, status):
        self.listener.queue().put(status.text, timeout = 0.01)
        return True
  
    def on_error(self, status_code):
        return True # keep stream alive
  
    def on_limit(self, track):
        return True # keep stream alive

    def on_data(self,data):
	dataJson = simplejson.loads(data[:-1])
        #self.dataJsonText = self.dataJson["text"].lower()


	try:
		dataJsonText = dataJson["text"].lower()
		self.spout.queue().put(dataJsonText, timeout = 0.1)
		print(dataJsonText + ' added to queue.')
 	
	except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            #pass
	    print("Can't load queue--(probably a queue overflow)")


class Tweets(Spout):

    def initialize(self, stormconf, context):
        self._queue = Queue.Queue(maxsize = 10000)

        consumer_key = auth_get("consumer_key") 
        consumer_secret = auth_get("consumer_secret") 
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	
        if auth_get("access_token") and auth_get("access_token_secret"):
            access_token = auth_get("access_token")
            access_token_secret = auth_get("access_token_secret")
            self.auth.set_access_token(access_token, access_token_secret)

        self._tweepy_api = tweepy.API(self.auth)

        # Create the listener for twitter stream
        self.listener = TweetStreamListener(self)

        # Create the stream and listen for english tweets
        self.stream = tweepy.Stream(self.auth,self.listener, timeout=None)
        self.stream.filter(languages=["en"], track=["a", "the", "i", "you", "u"], async=True)

    def queue(self):
        #self.log('queue called')
	return self._queue

    def tweepy_api(self):
        return self._tweepy_api

    def next_tuple(self):
        #tweet = self.queue().get(timeout = 0.1)
	try:
            tweet = self.queue().get(timeout = 0.1) 
            #print("T: " +tweet)
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
