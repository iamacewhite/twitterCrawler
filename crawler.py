# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 17:36:58 2016

@author: Chunyan
"""

from twitter import *
from langdetect import detect
from datetime import datetime
import json, gzip, os, traceback
global DIR, cache1, cache2, MINIBATCH_SIZE, MAX_CACHE
DIR = 'tweets/'
cache1 = []
cache2 = []
MINIBATCH_SIZE = 100
MAX_CACHE = 200


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
        traceback.print_exc()
        raise SystemExit

def writeData():
    try:
        time = datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S")
        filename = time + ".json"
        with open(os.path.join(DIR, filename), 'wb') as file:
            for obj in cache2:
                file.write(obj)
        with open(os.path.join(DIR, filename), 'rb') as f_in, gzip.open(os.path.join(DIR, filename + '.gz'), 'wb') as f_out:
            f_out.writelines(f_in)
        os.remove(os.path.join(DIR, filename))
        print(" - written " + str(len(cache2)) + " tweets to files.")
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise SystemExit

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
