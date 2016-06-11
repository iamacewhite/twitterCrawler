# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 17:36:58 2016

@author: Chunyan
"""

from twitter import *
from langdetect import detect
from datetime import datetime
import json, gzip
global DIR, cache1, cache2, MINIBATCH_SIZE, MAX_CACHE
DIR = 'tweets/'
cache1 = []
cache2 = []
MINIBATCH_SIZE = 160
MAX_CACHE = 3000


def sendMiniBatch():
    global cache2
    try:
        for item in cache1:
            cache2.append(item)
            if len(cache2) > MAX_CACHE:
                writeData()
                cache2 = []
    except Exception as e:
        print(e)

def writeData():
    time = datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S")
    filename = DIR + time + ".json"
    with open(filename, 'wb') as file:
        for obj in cache2:
            file.write(obj)
    with open(filename) as f_in, gzip.open(filename + '.gz', 'wb') as f_out:
        f_out.writelines(f_in)
    os.remove(filename)
    print(" - written " + len(cache2) + " tweets to files.")

twitter_stream = TwitterStream(auth=OAuth(
                       "226621933-UjykmlKE2K2XAH9EJQPALqzite4iODoI0dj2WxOw", # OAUTH_TOKEN
                       "K3Wh16frHVGuqYaIKImWHMLtEyKjUVm75vRaPtAE4Y", # OAUTH_SECRET,
                       "XaReMlNq2kzDR2JIEuQuQ", # CONSUMER_KEY,
                       "HAR2c3LywOsIGqRYgr1nYC4FJtiBAK3CY6Uw4r1dePg" # CONSUMER_SECRET
                       ))
while True:
    iterator = twitter_stream.statuses.sample()

    for tweet in iterator:
        tweet = json.loads(json.dumps(tweet))
        try:
            text = tweet['text']
            if detect(text) == 'en' and len(text) >= 10:
                text = str(tweet) + '\n'
                cache1.append(text.encode('utf-8'))
                if len(cache1) % 100 is 0:
                    print("crawled " + str(len(cache1)) + "...")
                if len(cache1) >= MINIBATCH_SIZE:
                    sendMiniBatch()
                    cache1 = []
        except Exception as e:
            print(e)

        


        
    