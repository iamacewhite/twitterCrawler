# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 17:36:58 2016

@author: Chunyan
"""

from twitter import *
from langdetect import detect
from datetime import datetime
import json, gzip, os, traceback, sys

def sendMiniBatch(cache1, cache2, MAX_CACHE, DIR):
    try:
        for item in cache1:
            cache2.append(item)
            if len(cache2) >= MAX_CACHE:
                writeData(cache2, DIR)
                del cache2[:]
    except KeyboardInterrupt:
        print str(datetime.now()) + " program exit\n"
        raise SystemExit
    except Exception as e:
        print str(datetime.now()) + ' ' + str(e) + '\n'
        traceback.print_exc()
        raise SystemExit

def writeData(cache2, DIR):
    try:
        time = datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S")
        filename = time + ".json"
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        data = []
        for obj in cache2:
            data.append(obj)
        with open(os.path.join(DIR, filename), 'wb') as file:
            file.write(json.dumps(data))
        with open(os.path.join(DIR, filename), 'rb') as f_in, gzip.open(os.path.join(DIR, filename + '.gz'), 'wb') as f_out:
            f_out.writelines(f_in)
        os.remove(os.path.join(DIR, filename))
        print str(datetime.now()) + " - written " + str(len(cache2)) + " tweets to files."
    except KeyboardInterrupt:
        print str(datetime.now()) + " program exit\n"
        raise SystemExit
    except Exception as e:
        print str(datetime.now()) + ' ' + str(e) + '\n'
        traceback.print_exc()
        raise SystemExit



def crawl(twitter_stream, cache1, cache2, MINIBATCH_SIZE, MAX_CACHE, DIR):
    #infinite loop for retriving tweets
    while True:
        iterator = twitter_stream.statuses.sample()
        for tweet in iterator:
            tweet = json.loads(json.dumps(tweet))
            try:
                text = tweet['text']
                if detect(text) == 'en' and len(text) >= 10:
                    text = str(tweet) + '\n'
                    cache1.append(text.encode('utf-8'))
                    if len(cache1) % 1000 is 0:
                        print str(datetime.now()) + "crawled " + str(len(cache1)) + "..."
                    if len(cache1) >= MINIBATCH_SIZE:
                        sendMiniBatch(cache1, cache2, MAX_CACHE, DIR)
                        del cache1[:]
            except KeyboardInterrupt:
                print str(datetime.now()) + " program exit\n"
                raise SystemExit
            except Exception as e:
                print str(datetime.now()) + ' ' + str(e) + '\n'

if __name__ == "__main__":
    sys.stdout = open('crawler.log', 'a+')
    twitter_stream = TwitterStream(auth=OAuth(
                           "226621933-UjykmlKE2K2XAH9EJQPALqzite4iODoI0dj2WxOw", # OAUTH_TOKEN
                           "K3Wh16frHVGuqYaIKImWHMLtEyKjUVm75vRaPtAE4Y", # OAUTH_SECRET,
                           "XaReMlNq2kzDR2JIEuQuQ", # CONSUMER_KEY,
                           "HAR2c3LywOsIGqRYgr1nYC4FJtiBAK3CY6Uw4r1dePg" # CONSUMER_SECRET
                           ))
    DIR = 'tweets/'
    cache1 = []
    cache2 = []
    MINIBATCH_SIZE = 160
    MAX_CACHE = 300
    crawl(twitter_stream, cache1, cache2, MINIBATCH_SIZE, MAX_CACHE, DIR)
