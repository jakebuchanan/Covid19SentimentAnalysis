# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:57:36 2020

@author: jakeb
"""

#to install libraries do 'pip install NAME' without the quotes
#pip install tweepy
#pip install textblob

#libraries needed
import tweepy
import re
from textblob import TextBlob
import csv
import time
#optional library for other form of sentiment analysis
#from textblob.sentiments import NaiveBayesAnalyzer

#create csvs for each demographic
csvFile0 = open('midwestLocalCOVID.csv','a')
csvFile1 = open('midwestRTCOVID.csv','a')
csvFile2 = open('nycLocalCOVID.csv','a')
csvFile3 = open('nycRTCOVID.csv','a')
csvFile4 = open('californiaLocalCOVID.csv','a')
csvFile5 = open('californiaRTCOVID.csv','a')
csvFile6 = open('southLocalCOVID.csv','a')
csvFile7 = open('southRTCOVID.csv','a')
csvFile8 = open('italyLocalCOVID.csv','a')
csvFile9 = open('italyRTCOVID.csv','a')
csvFile10 = open('midwestLocalRona.csv','a')
csvFile11 = open('midwestRTRona.csv','a')
csvFile12 = open('nycLocalRona.csv','a')
csvFile13 = open('nycRTRona.csv','a')
csvFile14 = open('californiaLocalRona.csv','a')
csvFile15 = open('californiaRTRona.csv','a')
csvFile16 = open('southLocalRona.csv','a')
csvFile17 = open('southRTRona.csv','a')
csvFile18 = open('italyLocalRona.csv','a')
csvFile19 = open('italyRTRona.csv','a')

#csvwriters for each of the csvs
csvWriter0 = csv.writer(csvFile0)
csvWriter1 = csv.writer(csvFile1)
csvWriter2 = csv.writer(csvFile2)
csvWriter3 = csv.writer(csvFile3)
csvWriter4 = csv.writer(csvFile4)
csvWriter5 = csv.writer(csvFile5)
csvWriter6 = csv.writer(csvFile6)
csvWriter7 = csv.writer(csvFile7)
csvWriter8 = csv.writer(csvFile8)
csvWriter9 = csv.writer(csvFile9)
csvWriter10 = csv.writer(csvFile10)
csvWriter11 = csv.writer(csvFile11)
csvWriter12 = csv.writer(csvFile12)
csvWriter13 = csv.writer(csvFile13)
csvWriter14 = csv.writer(csvFile14)
csvWriter15 = csv.writer(csvFile15)
csvWriter16 = csv.writer(csvFile16)
csvWriter17 = csv.writer(csvFile17)
csvWriter18 = csv.writer(csvFile18)
csvWriter19 = csv.writer(csvFile19)

#array to index csvwriters
csvWriters = [csvWriter0,
              csvWriter1,
              csvWriter2,
              csvWriter3,
              csvWriter4,
              csvWriter5,
              csvWriter6,
              csvWriter7,
              csvWriter8,
              csvWriter9,
              csvWriter10,
              csvWriter11,
              csvWriter12,
              csvWriter13,
              csvWriter14,
              csvWriter15,
              csvWriter16,
              csvWriter17,
              csvWriter18,
              csvWriter19
              ]

#twitter authentication
auth = tweepy.OAuthHandler(
'2D9xjayGq5WFlqSHJdRvfx4cS',
'bfEuCh1qnlYlGUYYhSY1pLjAUqu6A0uQguVqRkFi3VZRx5fVAK')

auth.set_access_token('1244691819990040577-slfyd39ZSx99cM2Xl32TV3UZV74cTO',
                      '7rJ7o24qb4nLNWMKEJQxiP8Sxv9SamDs2stM0lpiIpfJI')

api = tweepy.API(auth)


#regex to normalize tweets
def cleanTweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

#function that uses twitter api search to find 100 tweets related to search_keyword from a given location
def buildTestSet(search_keyword,location):
    try:
        tweets_fetched = api.search(search_keyword, count = 100, lang = 'en', geocode = location)
        return [cleanTweet(status.text) for status in tweets_fetched]
    except:
        print("Unfortunately, something went wrong..")
        return None
    
#function that parses nonRts from testSet
def localDataSet(dataset):
    newSet = []
    for tweet in dataset:
        if tweet[0:2] != 'RT':
            newSet.append(tweet)
    
    return newSet

#function that parses Rts from testSet
def RTDataSet(dataset):
    newSet = []
    for tweet in dataset:
        if tweet[0:2] == 'RT':
            newSet.append(tweet)
    return newSet

#pass tweet into function to be classified in one of six sentiments
#polarity is a float from [-1,1] which classifies if a tweet is positive,neutral,negative
#subjectivity is a float from [0,1] which classifies if a tweet is subjective or objective
def sentimentAnalyzer(tweet):
    
    #blob = TextBlob(tweet, analyzer=NaiveBayesAnalyzer())
    #return blob.sentiment
    # nltk version
    
    blob = TextBlob(tweet)
    if blob.sentiment.polarity > 0: #positive
        if blob.sentiment.subjectivity >= .5: #subjective
            return 'positive subjective'
        else: #objective
            return 'positive objective'
    elif blob.sentiment.polarity == 0: #neutral
        if blob.sentiment.subjectivity >= .5: #subjective
            return 'neutral subjective' 
        else: #objective
            return 'neutral objective'
    else: #negative
        if blob.sentiment.subjectivity >= .5: #subjective
            return 'negative subjective'
        else: #objective
            return 'negative objective'
        
def sentimentScore(tweet):
    blob = TextBlob(tweet)
    print("Polarity & Subjectivity Scores: (" + str(blob.sentiment.polarity) + ", " + str(blob.sentiment.subjectivity) + ')\n')
 
    
#coordinates and radius for five locations to search from
locations = ['44.986656,-93.258133,5mi', #Minneapolis
             '40.730610,-73.935242,5mi', #NYC
             '37.773972,-122.431297,5mi', #San Francisco
             '30.8310841,-88.098057,10mi', #Saraland, Alabama
             '51.509865,-0.118092,5mi' #Venice, Italy
             ]

places = ['Minneapolis, Minnesota',
          'New York City, New York',
          'San Francisco, California',
          'Saraland, Alabama',
          'Venice, Italy'
          ]

count = 0
csvCount = 0

print("COVID-19 Data Sets")
#loop through tweets from the five locations
while count < 5:
    
    #build the two data sets
    testDataSetLocal = localDataSet(buildTestSet("COVID-19",locations[count]))
    testDataSetRT = RTDataSet(buildTestSet("COVID-19",locations[count]))
    
    #create a dictionary for counts with each given sentiment
    sentiment_dict = {"positive subjective":0,
                  "positive objective":0,
                  "neutral subjective":0,
                  "neutral objective":0,
                  "negative subjective":0,
                  "negative objective":0}
    
    sentiment_dict_RT = sentiment_dict
    
    print(places[count])
    
    #classify tweets in local set
    for tweet in testDataSetLocal:
        csvWriters[csvCount].writerow([tweet,sentimentAnalyzer(tweet)])
        sentiment_dict[sentimentAnalyzer(tweet)] += 1
    print('Local Set Sentiments')
    print(sentiment_dict)
    
    csvCount = csvCount + 1
    #classify tweets in RT set
    for tweet in testDataSetRT:
        csvWriters[csvCount].writerow([tweet,sentimentAnalyzer(tweet)])
        sentiment_dict_RT[sentimentAnalyzer(tweet)] += 1
    print('RT Set Sentiments')
    print(sentiment_dict_RT)
    print('\n')
    
    csvCount = csvCount + 1
    count = count + 1
    
count = 0
#loop through tweets from the five locations
print("Rona data sets")
while count < 5:
    
    #build the two data sets
    testDataSetLocal = localDataSet(buildTestSet("rona",locations[count]))
    testDataSetRT = RTDataSet(buildTestSet("rona",locations[count]))
    
    #create a dictionary for counts with each given sentiment
    sentiment_dict = {"positive subjective":0,
                  "positive objective":0,
                  "neutral subjective":0,
                  "neutral objective":0,
                  "negative subjective":0,
                  "negative objective":0}
    
    sentiment_dict_RT = sentiment_dict
    
    print(places[count])
    
    #classify tweets in local set
    for tweet in testDataSetLocal:
        csvWriters[csvCount].writerow([tweet,sentimentAnalyzer(tweet)])
        sentiment_dict[sentimentAnalyzer(tweet)] += 1
    print('Local Set Sentiments')
    print(sentiment_dict)
    
    csvCount = csvCount + 1
    #classify tweets in RT set
    for tweet in testDataSetRT:
        csvWriters[csvCount].writerow([tweet,sentimentAnalyzer(tweet)])
        sentiment_dict_RT[sentimentAnalyzer(tweet)] += 1
    print('RT Set Sentiments')
    print(sentiment_dict_RT)
    print('\n')
    
    csvCount = csvCount + 1
    count = count + 1
  
#close open files
csvFile0.close()
csvFile1.close()
csvFile2.close()
csvFile3.close()
csvFile4.close()
csvFile5.close()
csvFile6.close()
csvFile7.close()
csvFile8.close()
csvFile9.close()
csvFile10.close()
csvFile11.close()
csvFile12.close()
csvFile13.close()
csvFile14.close()
csvFile15.close()
csvFile16.close()
csvFile17.close()
csvFile18.close()
csvFile19.close()

  


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        time.sleep(5)
        print(status.text + '\n' + "Sentiment: " + sentimentAnalyzer(status.text))
        sentimentScore(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False
                
        

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track = ['rona','COVID-19'], languages = ['en'], locations =[ -93.258133,  44.986656, -92.100487 , 46.786671 ] )



    

