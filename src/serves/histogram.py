

def fetchRecords():
	import psycopg2
	conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
	cur = conn.cursor()
	cur.execute('''SELECT * FROM tweetwordcount ORDER BY count DESC;''')
	records = cur.fetchall()
	conn.commit()
	conn.close()

	return records


def main():
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-v", "--verbose", action = "store_true")

	(options, args) = parser.parse_args()
	recs = fetchRecords()
	#print recs
	if len(args) > 0:
		minhits = int(args[0].split(',')[0])
		maxhits = int(args[0].split(',')[1])
		
		for r in recs:
			#print r[2]
			if (r[2]>=minhits) and (r[2]<=maxhits):
				print r[1] + ': ' + str(r[2])
	else:
		print "Error.  Ensure command follows the form of python histogram.py 3,8"

	


if __name__ == '__main__':
	main()


