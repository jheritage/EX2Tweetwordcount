#!/bin/bash


cp ./pg_hba.conf /var/lib/pgsql/data/pg_hba.conf
cd /data
git init
git clone https://github.com/pulsetracker/W205-Ex2.git
sudo yum install python27-devel –y
sudo curl -o ez_setup.py https://bootstrap.pypa.io/ez_setup.py
sudo python ez_setup.py
sudo easy_install-2.7 pip
pip install virtualenv
wget --directory-prefix=/usr/bin/ https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
chmod a+x /usr/bin/lein
sudo /usr/bin/lein
pip install streamparse
pip install psycopg2
pip install tweepy
sudo pip install requests==2.5.3


echo "Make sure you set up your twitter credentials!"
echo "Put them at the top of EX2Tweetwordcount/src/spouts/tweets.py"

# Stuff used in initial setup
#git clone https://github.com/UC-Berkeley-I-School/w205-labs-exercises.git
#sparse quickstart EX2Tweetwordcount
#cp -R ../w205-labs-exercises/exercise_2/tweetwordcount/* 
