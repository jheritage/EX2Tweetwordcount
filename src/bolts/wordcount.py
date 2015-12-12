from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt



class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

	import psycopg2
	
	#clear database of old words
        conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

        cur = conn.cursor()
	cur.execute('''DELETE FROM tweetwordcount''')
       	conn.commit()
        conn.close()


    def process(self, tup):
	import psycopg2

        word = tup.values[0].replace("'","").replace("`","")

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: Tcount 
        # Table name: Tweetwordcount 
        # you need to create both the database and the table in advance.
        

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])

	conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
	cur = conn.cursor()
	if self.counts[word] == 1:  #if this is the first time the word was seen
		query = "INSERT INTO tweetwordcount (word,count) VALUES ('" + word + "',1);"
		#cur.execute("INSERT INTO tweetwordcount (word,count) VALUES (%s, 1)", (word))
		self.log("Query: " + query)
		cur.execute(query)
		conn.commit()
	else:
		uCount = self.counts[word]
		query = "UPDATE tweetwordcount SET count=" + str(uCount) + " WHERE word='" + word + "';"
		cur.execute(query)
		conn.commit()


        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))
