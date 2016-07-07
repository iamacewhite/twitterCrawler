# -*- coding: utf-8 -*-
import re
from nltk.stem import *

class preprocessing(object):

  def __init__(self):
    self.doStemming = True
    self.removeNonAlpha = True
    self.removeUsernames = True
    self.stem = PorterStemmer()
    
  def clean(self, tweet):
      return self.cleanTweetForExport(tweet)

  def cleanTweetForExport(self, tweet):
    if tweet is None or len(tweet) is 0:
      return ""
    stoplist = []
    with open('english.stop.txt', 'r') as f:
         stoplist = f.read().splitlines()
    tweet = self.stripTweet(tweet)
    tweet = self.cleanUpTerm(tweet, False)
    if self.removeNonAlpha:
      tweet = self.removeNonAlphaCharacters(tweet)
    tweet = self.stemAndRemoveStopwords(tweet, stoplist)
    while "  " in tweet:
      tweet = tweet.replace("  ", " ")
    return tweet

  def stripTweet(self, tweet):
    tweet = tweet.replace("@", "#at#")  #avoid removing @-symbols
    tweet = tweet.lower()
    tweet = tweet.replace("\"", " ").replace("\n", " ")
    #tweet = tweet.replaceAll("[“”’°]", " ")
    tweet = re.sub("[“”’°]", " ", tweet)
    tweet = re.sub("&[a-zA-Z0-9]+;", " ", tweet)  #replace HTML encoded characters
    tweet = re.sub("(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]", " ", tweet)  #replace URLs
    tweet = re.sub("[\\.:,&\\(\\)\\-_\\?!/]", " ", tweet)  #replace punctuation
    tweet = tweet.replace("#at#", "@")  #avoid removing @-symbols
    tweet = tweet.replace("@", " @")
    tweet = tweet.replace("#", " #")
    while True:
      a = re.search("(\\w)\\1\\1+", tweet)
      if a:
        repeated = a.group()
        tweet = tweet.replace(repeated, repeated[:2])
      else:
        break

    while "  " in tweet:
        tweet = tweet.replace("  ", " ")
    tweet = tweet.strip()

    if self.removeUsernames and "@" in tweet:
        words = tweet.split(" ")
        output = ""
        for w in words:
            if not w[0] == "@":
                output += " " + w
        tweet = output.strip()
    return tweet


  def cleanUpTerm(self, term, removeNonWords):
    term = re.sub("(\\s)+|/|\\p{Punct}{2,}", " ", term)
    term = re.sub("\\p{Punct}", "", term) # single punctuation
    term = re.sub("(\\d)+", "", term) # remove numbers
    term = term.replace("http", "")
  #        term = term.replace("�", "").replace("�s", "").replace("'s", "")
  #        term = term.replace("�", "").replace("�", "")
    term = term.replace("’s", "").replace("'s", "").replace("…", " ").replace("‘", " ")
    if removeNonWords:
        term = re.sub("\\W", "", term)
    term = term.replace("ß", "ss")  #fix for a SQL bug (SQL server 2012)
    term = term.strip()
    return term

  def removeNonAlphaCharacters(self, line):
    line = re.sub("\t", " ", line)
    line = re.sub("[^a-zA-Z0-9#-_ ]", "", line)
    return line

  def stemAndRemoveStopwords(self, tweet, stoplist):
    terms = tweet.split(" ")
    output = ""
    for term in terms:
        if term in stoplist or term == "rt" or len(term)<2:
            continue
        if self.doStemming:
            term = self.stem.stem(term)
        output += " " + term

    output = output.strip()
    return output
