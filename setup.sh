#!/bin/bash


cd /data
# Install necessary libraries
sudo yum install -y python27-devel 
sudo curl -o ez_setup.py https://bootstrap.pypa.io/ez_setup.py
sudo python ez_setup.py
sudo easy_install pip
pip install virtualenv
wget --directory-prefix=/usr/bin/ https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
chmod a+x /usr/bin/lein
export LEIN_ROOT="ok"
sudo /usr/bin/lein
pip install streamparse
pip install psycopg2
pip install tweepy
sudo pip install requests==2.5.3

# setup postgres
sudo yum install -y postgresql
sudo service postgresql initdb
cp  /data/EX2Tweetwordcount/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf
sudo service postgresql start

echo "Waiting 20 seconds to let the database server get up and going"
sleep 20

# setup the postgres database
su -l postgres -c 'psql -d postgres -U postgres -f /data/EX2Tweetwordcount/dbsetup.sql'


echo " "
echo "           Make sure you set up your twitter credentials!"
echo "           Put them at the top of EX2Tweetwordcount/src/spouts/tweets.py"
echo "           vim src/spouts/tweets.py should do it "
echo " "

# Stuff used in initial setup
#git clone https://github.com/UC-Berkeley-I-School/w205-labs-exercises.git
#sparse quickstart EX2Tweetwordcount
#cp -R ../w205-labs-exercises/exercise_2/tweetwordcount/* 
