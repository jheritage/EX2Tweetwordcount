#!/bin/bash

cd /data
git init
git clone https://github.com/UC-Berkeley-I-School/w205-labs-exercises.git
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
sparse quickstart EX2Tweetwordcount
cd EX2Tweetwordcount
cp -R ../w205-labs-exercises/exercise_2/tweetwordcount/* .

pip install tweepy

echo "Make sure you set up your twitter credentials!"
# Upgrade to python 2.7.10 so that SSL works`:
#cd /usr/src
#wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
#tar xzf Python-2.7.10.tgz
#cd Python-2.7.10
#./configure
#make altinstall
#export PATH=/usr/src/Python-2.7.10:$PATH

