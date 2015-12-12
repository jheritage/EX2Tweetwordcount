

def fetchRecords():
	import psycopg2
	conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
	cur = conn.cursor()
	cur.execute('''SELECT * FROM tweetwordcount ORDER BY word ASC;''')
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
	if len(args) > 0:
		searchword = args[0]
		for r in recs:
			if r[1]==searchword:
				print "Total number of occurances of '"+ searchword + "': " + str(r[2])
				return
		print "Total number of occurances of '"+ searchword + "': " + str(0)
	else:
		print [(r[1],r[2]) for r in recs]

	


if __name__ == '__main__':
	main()


