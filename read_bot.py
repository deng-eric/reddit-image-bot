
#!/usr/bin/python
import praw
from imgurpython import ImgurClient
import requests
import os
from cfg import *
import urllib
import sys
import datetime
import re

#INITIALIZATION IS DEFINED IN CFG.PY
# REDDIT API INITIALIZATION
reload(sys)
sys.setdefaultencoding('utf-8')
reddit = praw.Reddit(client_id=rclient_id,
                     client_secret=rclient_secret, password=rpassword,
                     user_agent=ruser_agent, username=rusername)
subreddit = reddit.subreddit(sub)

#IMGUR API INITIALIZATION
imgur = ImgurClient(iclient_id, iclient_secret)

def isReddit(url):
    url_regex = re.compile('^(?:https?://)i\.redd\.it/(.*[^\/])')
    regex_match = re.match(url_regex, url)
    if regex_match == None:
        return False
    else:
        return True

def isImgur(url):
    imgur   = re.match(r'^(http|https)\:\/\/imgur\.com', url, re.M|re.I)
    album   = re.match(r'^(http|https)\:\/\/imgur\.com\/(a|gallery)\/', url, re.M|re.I)
    direct  = re.match(r'.*\.jpg', url, re.M|re.I)

    if direct:
        urlType = "direct"
    elif album:
        urlType = "album"
    elif imgur:
        urlType = "imgur"
    else:
        urlType = "unknown"
    return urlType

def download(title, path, filename, url):
    print datetime.datetime.now().time()
    print '/r/' + path + '/' + title
    print url  + '\n'  
    if not os.path.exists(path):
        os.makedirs(path)
    urllib.urlretrieve(url, path+"/"+filename)

def handleDirect(submission):
    filename = submission.url.split('/')[-1]
    path = str(submission.subreddit)
    url =  str(submission.url)
    title = str(submission.title)
    download(title, path, filename, url)

def handleImgur(submission): #is an imgur page
    filename = submission.url.split('/')[-1] + ".jpg"
    path = str(submission.subreddit)
    url = "https://i.imgur.com/{}.jpg".format(filename)
    title = str(submission.title)
    download(title, path, filename, url)

def handleImgurAlbum(submission):
    path = str(submission.subreddit)
    title = str(submission.title)

    albumID = submission.url.split('/')[-1]
    albumImages = imgur.get_album_images(albumID)

    print '/r/' + path + '/' + title
    print str(submission.url) 
    for albumImage in albumImages:
        url = albumImage.link
        filename = url.split('/')[-1]
        download(title, path, filename, url)

for submission in subreddit.stream.submissions():
    if isReddit(submission.url):
        handleDirect(submission)
    elif isImgur(submission.url) == 'imgur':
        handleImgur(submission)
    elif isImgur(submission.url) == 'direct':
        handleDirect(submission)
    elif isImgur(submission.url) == 'album':
        handleImgurAlbum(submission)

