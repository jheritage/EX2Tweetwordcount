from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt



class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

	import psycopg2

        conn = psycopg2.connect(database="Tcount", user="postgres", password="", host="localhost", port="5432")

        cur = conn.cursor()
	try:
	        cur.execute('''CREATE TABLE Tweetwordcount
                        (
                        word TEXT PRIMARY KEY     NOT NULL,
                        count INT     NOT NULL);''')
        	conn.commit()
	        conn.close()
	except:
 		self.log('Error trying to add table to database--it probably already exists.')


    def process(self, tup):
	import psycopg2

        word = tup.values[0]

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: Tcount 
        # Table name: Tweetwordcount 
        # you need to create both the database and the table in advance.
        

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])

	conn = psycopg2.connect(database="Tcount", user="postgres", password="pass", host="localhost", port="5432")

	if self.counts[word] == 1:  #if this is the first time the word was seen
		cur.execute("INSERT INTO Tweetwordcount (word,count) VALUES (%s, 1)", word)
		conn.commit()
	else:
		uCount = self.counts[word]
		cur.execute("UPDATE Tweetwordcount SET count=%s WHERE word=%s", (word, uCount))
		conn.commit()


        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))
