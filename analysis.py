# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 19:07:29 2017

@author: michael
"""

import os
import re
import csv
from textblob import TextBlob
from matplotlib import pyplot as plt


os.chdir(r"D:\Projects\Party-Platform-Analysis\\")
platforms = os.listdir("platforms-raw")


platformCorpus = {}
for plat in platforms:
    with open("platforms-raw/%s" %(plat), 'r', encoding='utf-8') as f:
        year = re.search("\d{4}", plat).group()
        party = plat.replace(year,'').replace("of ",'').replace(".txt",'').replace("the ",'').replace("Platform",'').strip()
        platformCorpus[plat] = {'full-text':f.read(),
                                'year': year,
                                'party': party}

        
        
        
sentimentDict = {}        
for plat in platforms:
    text = TextBlob(platformCorpus[plat]['full-text'])
    platformCorpus[plat]['sentiment'] = text.sentiment.polarity
    sentimentDict[plat] = text.sentiment.polarity
    
 
dem_year = []
dem_sent = []
rep_year = []
rep_sent = []
   
for plat in platforms:
    if platformCorpus[plat]['party'] == "Democratic Party":
        dem_year.append(platformCorpus[plat]['year'])
        dem_sent.append(platformCorpus[plat]['sentiment'])
    if platformCorpus[plat]['party'] == "Republican Party":
        rep_year.append(platformCorpus[plat]['year'])
        rep_sent.append(platformCorpus[plat]['sentiment'])
    

dem_year, dem_sent = (list(t) for t in zip(*sorted(zip(dem_year, dem_sent))))
rep_year, rep_sent = (list(t) for t in zip(*sorted(zip(rep_year, rep_sent))))

transitions = []
with open('transitions.csv', 'r') as infile:
     reader = csv.reader(infile)
     for row in reader:
         transitions.append(row)
         
transitions.pop(0)
t_colors = {"Whig": 'w', "Democrat": 'b', "Republican": 'r'}

plt.figure(figsize=(20,7))

line1, = plt.plot(dem_year, dem_sent, label="Democratic Party", color="blue")
line2, = plt.plot(rep_year, rep_sent, label="Republican Party", color="red")
plt.xlim(1840,2020)
plt.legend()
plt.title('Party Platform Sentiment')

for row in transitions:
    plt.axvspan(int(row[0]), int(row[1]), color=t_colors[row[2]], alpha=0.5, lw=0)
    

plt.savefig('party-platform-sentiment.png')