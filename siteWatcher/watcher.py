"""
    Site Watcher
    To monitor sitemap xml file to check for any updates to web pages.
    Also implement site searching in text and images

    [ ]Monitor sitemap for latest modified pages
    [ ]Search through text
    [ ]Search through images using opencv

"""

import os

from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
from datetime import datetime
import re

DEBUG_MODE = True

def debugPrint(*args):
	if DEBUG_MODE:
		print("#"*3+"DEBUG --> ",end="")
		output = []
		for arg in args:
			output.append(arg)	
		print(output)

def webCrawl():
	#create dictionary of web links and if visited and visit time.
	pass


	#take in domain and parse sitemap.xml for more xml's and urls of weblinks and their lastModified date

def checkLastModified():
	print("#"*20)
	print("Check started at:" + str(datetime.now().time()))
	
    #function this
	url = "https://au.wilson.com/"
	sitemapURL = url + "sitemap.xml"
	print('url page:' + url)
	req = Request(
        url=sitemapURL, 
        headers={'User-Agent': 'Mozilla/5.0'}
	)
	content = urlopen(req).read()

	#content = urllib.request.urlopen(url).read()
	xmlSoup = BeautifulSoup(content, 'xml') #xml is the default xml parser can check for new ones
	    
	siteXMLs = []
	pageDictionary = {}
	
	for xmlURL in xmlSoup.find_all('loc'):
		siteXMLs.append(xmlURL.get_text())
		        
	debugPrint(siteXMLs)

	for xmlURL in siteXMLs:
		content = urllib.request.urlopen(xmlURL).read()
		urlSoup = BeautifulSoup(content, 'xml')
		for page in urlSoup.find_all('url'):
			pageUrl = page.find('loc').text #url should search for these tags specifically
			lastmodFind = page.find('lastmod')
			if lastmodFind:
				pageLastMod = lastmodFind.text #lastmod
			imageFind = page.find('image:image')
			if imageFind:
				imageFindLoc = imageFind.find('image:loc').text #image location
			else:
				imageFindLoc = ""
			pageChangeFreq = page.get_text().split('\n')[3] #changefreq
			if lastmodFind:
				pageDictionary[pageLastMod] = (pageUrl,imageFindLoc)
            
	print(10*"-","Summary",10*"-")
	recentPages = sorted(pageDictionary.items(), reverse=True)
	for x in range(10):
		print(recentPages[x])
		
#=========MAIN Function=============

if __name__ == '__main__':
	
	watcher = checkLastModified() 

