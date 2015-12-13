bash setup.sh


README.txt

James King
W205-2 -- Spring 2015



To get this app a-runnin’:

  1) Set up a Twitter application:  https://apps.twitter.com/.   Make note of your access keys.

  2) Spin up AWS EC2 Instance (m3.medium has been tested) with image ami-003f7f6a

  3) Login to the instance via ssh & run these commands (you might need to enter a gitHub password)

cd /data
git init
git clone https://github.com/pulsetracker/W205-Ex2.git
cd EX2Tweetwordcount
bash setup.sh  #this might take a while--it’s downloading and installing lots of software

# whenever you see this (you’ll see it more than once):
#    WARNING: You're currently running as root; probably by accident.
#    Press control-C to abort or Enter to continue as root.
#    Set LEIN_ROOT to disable this warning.
# press return

# Edit the file EX2Tweetwordcount/src/spouts/tweets.py and insert your twitter app credentials at the indicated positions starting at line 15

sparse run   #this will actually run the app -- there’s another LEIN_ROOT warning here

# Exit with Ctrl-C

cd /data/EX2Tweetwordcount/src/serves
python finalresults.py <word of interest>
python histogram.py 5,8


# If you try to restart and start to get Empty queue error like this:
# 27914 [Thread-20-tweet-spout] INFO  backtype.storm.spout.ShellSpout - ShellLog pid:5839, name:tweet-spout Empty queue exception 
#
# You're probably being throttled down by the Twitter servers.  Run this to fix it:
#
#kill -9 `ps -ef | grep streamparse | grep -v grep | awk '{print $2}'`

