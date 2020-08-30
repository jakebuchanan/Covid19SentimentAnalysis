# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 00:02:51 2020

@author: jakeb
"""

import csv

#open csvs for each demographic
csvFile0 = open('midwestLocalCOVID.csv','r')
csvFile1 = open('midwestRTCOVID.csv','r')
csvFile2 = open('nycLocalCOVID.csv','r')
csvFile3 = open('nycRTCOVID.csv','r')
csvFile4 = open('californiaLocalCOVID.csv','r')
csvFile5 = open('californiaRTCOVID.csv','r')
csvFile6 = open('southLocalCOVID.csv','r')
csvFile7 = open('southRTCOVID.csv','r')
csvFile8 = open('italyLocalCOVID.csv','r')
csvFile9 = open('italyRTCOVID.csv','r')
csvFile10 = open('midwestLocalRona.csv','r')
csvFile11 = open('midwestRTRona.csv','r')
csvFile12 = open('nycLocalRona.csv','r')
csvFile13 = open('nycRTRona.csv','r')
csvFile14 = open('californiaLocalRona.csv','r')
csvFile15 = open('californiaRTRona.csv','r')
csvFile16 = open('southLocalRona.csv','r')
csvFile17 = open('southRTRona.csv','r')
csvFile18 = open('italyLocalRona.csv','r')
csvFile19 = open('italyRTRona.csv','r')

cities = ['midwestLocal',
          'midwestRT',
          'nycLocal',
          'nycRT',
          'californiaLocal',
          'californiaRT',
          'southLocal',
          'southRT',
          'italyLocal',
          'italyRT',          
          ]

csvReader0 = csv.reader(csvFile0)
csvReader1 = csv.reader(csvFile1)
csvReader2 = csv.reader(csvFile2)
csvReader3 = csv.reader(csvFile3)
csvReader4 = csv.reader(csvFile4)
csvReader5 = csv.reader(csvFile5)
csvReader6 = csv.reader(csvFile6)
csvReader7 = csv.reader(csvFile7)
csvReader8 = csv.reader(csvFile8)
csvReader9 = csv.reader(csvFile9)
csvReader10 = csv.reader(csvFile10)
csvReader11 = csv.reader(csvFile11)
csvReader12 = csv.reader(csvFile12)
csvReader13 = csv.reader(csvFile13)
csvReader14 = csv.reader(csvFile14)
csvReader15 = csv.reader(csvFile15)
csvReader16 = csv.reader(csvFile16)
csvReader17 = csv.reader(csvFile17)
csvReader18 = csv.reader(csvFile18)
csvReader19 = csv.reader(csvFile19)

csvReaders = [csvReader0,
              csvReader1,
              csvReader2,
              csvReader3,
              csvReader4,
              csvReader5,
              csvReader6,
              csvReader7,
              csvReader8,
              csvReader9,
              csvReader10,
              csvReader11,
              csvReader12,
              csvReader13,
              csvReader14,
              csvReader15,
              csvReader16,
              csvReader17,
              csvReader18,
              csvReader19
              ]

count = 0
print("COVID-19 data sets")
for reader in csvReaders:
    sentiment_dict = {"positive subjective":0,
                  "positive objective":0,
                  "neutral subjective":0,
                  "neutral objective":0,
                  "negative subjective":0,
                  "negative objective":0}
    i = 0
    for row in reader:
        #row[0] is the tweet
        #row[1] is the sentiment
        if i % 2 == 0: #correct formatting
            sentiment_dict[row[1]] += 1
        
        i = i + 1
    if count == 10:
        print("Rona data sets")
        count = 0
    print(cities[count])
    print(max(sentiment_dict.items(), key=lambda k: k[1]))
    print('\n')
    count+=1
    
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