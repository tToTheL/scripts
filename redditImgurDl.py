#!/usr/bin/python2.7

# this script simply goes through a reddit subreddit, and downloads all the imgur images
# that have been posted in the subreddit, including albums, and throws all the images
# into a single folder.

# the script isn't designed to be easy to use, there are a few things that need to be
# configured, mostly, the download folder and the user agent

# --usage--
# subreddit less the "/r"
# post limit


# known problem:
# will not handle imgur links, where the picture ids are separated by commas in the url
# a llinked file like "...e.png?1" will not work right, I should just strip stuff after the question mark
# the count might be off by 1, or more

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


def imageDownload(img_url):
    filename =  img_url.rsplit('/', 1)[1]
    if not os.path.exists(script_path + dl_folder + filename):
        opener = urllib2.build_opener()
        response = opener.open(img_url)
        f = open(script_path + dl_folder + filename, 'w')
        f.write(response.read())
        f.close
        print "Downloaded: %s" % (filename)
        time.sleep(10)
        return True
    print "Skipped (already exists): %s" % (filename)
    return False




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

    if url[-3:] == 'jpg' or url[-3:] == 'peg' or url[-3:] == 'png' or url[-3:] == 'gif':
        # just download, we have a direct link
        imageDownload(url)
        new_count += 1
    else:
        opener = urllib2.build_opener()
        try:
            response = opener.open(url)
            html = response.read()
            tree = etree.HTML(html)
            els = tree.xpath("//div[@class='item view album-view-image-link']/a/@href")
            if len(els) == 0:
                els = tree.xpath("//a[@class='zoom']/@href")

            if len(els) == 0:
                els = tree.xpath("//div[@id='image']/div/a/@href")

            if len(els) == 0:
                els = tree.xpath("//div[@id='image']/div/img/@src")

            if len(els) == 0:
                els = tree.xpath("//div[@class='image textbox']/a/@href")



            if len(els) == 0:
                print ""
                print "Did not find imgur image at: %s" % (url)
                print "Could not find imgur link with post title: %s" % (x.__getattribute__('title'))
                print ""

            # if the link isn't imgur, this should be fine, it will just be a loop of zero
            for img_url in els:
                if imageDownload(img_url):
                    new_count += 1
        except:
            pass

print "%s new photos were added" % (str(new_count))

