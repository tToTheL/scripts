#!/usr/bin/python2.7

# this script simply goes through a reddit subreddit, and downloads all the imgur images
# that have been posted in the subreddit, including albums, and throws all the images
# into a single folder.

# the script isn't designed to be easy to use, there are a few things that need to be
# configured, mostly, the download folder and the user agent

# reddit API
import praw

# searching through HTML
from lxml import etree

# getting stuff from the Internet
import urllib2

# determining script path
import os

# determining path of script
import inspect

# built in delay to be nice to the servers
import time

# for command line arguments
import sys

# subreddit less the "/r"
# post limit

subreddit = str(sys.argv[1])
limit = int(sys.argv[2])

# this isn't meant to be user friendly
if len(subreddit) < 1 or limit < 1:
    print "Argument Error: quitting"
    exit (1)

script_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
# this folder must be manually created
dl_folder = 'dls/'

# there must be a file (useragent.txt) in the directory containing a user agent on the first line
user_agent = ""
try:
    f = open (script_path + "useragent.txt", 'r')
    user_agent = f.readline()
    if user_agent == "":
        raise
except:
    print "User agent error"
    exit (1)

r = praw.Reddit(user_agent=user_agent)
submissions = r.get_subreddit(subreddit).get_new(limit=limit)
new_count = 0
for x in submissions:
    url = x.__getattribute__('url')
    opener = urllib2.build_opener()
    try:
        response = opener.open(url)
        html = response.read()
        tree = etree.HTML(html)
        els = tree.xpath("//a[@class='zoom']/@href")

        # if the link isn't imgur, this should be fine, it will just be a loop of zero
        for img_url in els:
            filename =  img_url.rsplit('/', 1)[1]
            print filename
            if not os.path.exists(script_path + dl_folder + filename):
                time.sleep(10)
                opener = urllib2.build_opener()
                response = opener.open(img_url)
                f = open(script_path + dl_folder + filename, 'w')
                f.write(response.read())
                f.close
                new_count += 1
    except:
        pass

print "%s new photos were added" % (str(new_count))

