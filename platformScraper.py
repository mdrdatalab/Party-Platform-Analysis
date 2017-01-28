# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 23:04:55 2017

@author: michael
"""

import requests
from bs4 import BeautifulSoup

#start by scraping the page for links
result = requests.get("http://www.presidency.ucsb.edu/platforms.php")

soup = BeautifulSoup(result.content)
links = soup.find_all("a")
all_links = []

for x in links:
    all_links.append(x.attrs['href'])
    
#now that we've got all the links from the page, we need to find the ones to
#the party platforms. fortunate, these all follow the pattern of having "?pid="
platform_links = [x for x in all_links if '?pid=' in x]

#create a dictionary to hold the document title, and text of the platform
platforms = {}
for link in platform_links:
    plat_result = requests.get(link)
    plat_soup = BeautifulSoup(plat_result.content)
    platforms[plat_soup.find("title").text] = plat_soup.find_all("span", "displaytext")
    
#now for each title, write it to a file. The title split them into Democratic, Republican,
#and minor parties, and that was causing issues, so we just take the important bit, by
#splitting on the ":".
for title in platforms:
    with open('%s.txt' %(title.split(": ")[1]), 'wb') as f:
        f.write(platforms[title][0].text.encode('utf8'))
    
    