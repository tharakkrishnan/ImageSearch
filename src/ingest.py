#!/usr/bin/python
""" 
        Gathers images from the Cogniac flickr account and dumps into a temporary folder
"""

import flickrapi
import json
import urllib, urlparse

import os

from pprint import pprint
from sets import Set

API_KEY = u'c871b759c44a9c7d3ced100ba2cf4dd0'
API_SECRET = u'da8022494490182e'

INGEST_DIR = "/tmp/ingest"

def fetch_urls():
        urls = Set([])
        page = 1
        len_urls = 0
        flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format="parsed-json")
        while 1:
                try:
                        photos = flickr.photos.search(user_id="143060054@N02", tag="people", extras="url_o", per_page=500, page=page)
                        #https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
			[urls.add("https://farm{}.staticflickr.com/{}/{}_{}.jpg".format(p["farm"], p["server"], p["id"], p["secret"])) for p in photos["photos"]["photo"] ]
                        page += 1
                        if len_urls != len(urls):
                                len_urls = len(urls)
                        else:
                                print "Captured {} urls in the photo set!".format(len_urls)
                        	break
                except Exception as e:
                        print e
                        break
        return urls

def ensure_dir(f):
    d = os.path.dirname(f)
 

def download_images(urls):
        if not os.path.exists(INGEST_DIR):
                os.makedirs(INGEST_DIR)
	total = len(urls)
	cnt = 0
        for url in urls:
                image = urllib.URLopener()
                image.retrieve(url, "{}/{}".format(INGEST_DIR, url.replace("/","#"))) 
                cnt += 1
		print "downloaded {}/{}: {}".format(cnt, total,  url)
        return


if __name__=="__main__":
        urls = fetch_urls()
        download_images(urls)
