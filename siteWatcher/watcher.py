"""
    Site Watcher
    To monitor sitemap xml file to check for any updates to web pages.
    Also implement site searching in text and images

    [x]Monitor sitemap for latest modified pages
    [x]Crawl Domain for set of url links
    [ ]Search through text
    [ ]Search through images using opencv
    [ ]incorporate a gui using tkinter
    [ ]better obfuscation for url request to avoid http 403 forbidden errors

"""

import os

from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from datetime import datetime
import re

DEBUG_MODE = False

def debugPrint(*args):
    if DEBUG_MODE:
        print("#"*3+"DEBUG --> ",end="")
        output = []
        for arg in args:
            output.append(arg)	
        print(output)

def webCrawl():
    #create dictionary of web links and if visited and visit time.
        
    url = "https://au.wilson.com"
    domain = "https://au.wilson.com"
    
    linkSet = set()

    foundLinks = findLinks(url, linkSet, "1", domain)
    
    for link in foundLinks:
        newLinks = findLinks(link, linkSet, "2", domain)
        
    print(linkSet)


    #take in domain and parse sitemap.xml for more xml's and urls of weblinks and their lastModified date

def readURL(urlToRead: str):
    if urlToRead == "https://wdt.wilson.com/":
        pass
    else:
        url = urlToRead
        print('url page:' + url)
        req = Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        content = urlopen(req).read()
        return content

        #content = urllib.request.urlopen(url).read()

def findLinks(urlToSearch: str, linkSet: set, roundTag: str, siteDomain: str):
    try:
        content = readURL(urlToSearch)
        soup = BeautifulSoup(content, 'lxml')
        links = []
        for link in soup.find_all('a', href=True):
            if "https://" in link['href'] or "http://" in link['href'] :
                newLink = link['href']
            else:                
                newLink = siteDomain + link['href']
            
            if newLink in linkSet:
                pass
            else:
                linkSet.add(newLink)
                links.append(newLink)
                print(" "*4, newLink)

        print(f"Round {roundTag}: linkset size is {len(linkSet)}")
        return links
    
    except HTTPError or URLError as e:
        print(e,urlToSearch)
        

def checkLastModified():
    print("#"*20)
    print("Check started at:" + str(datetime.now().time()))
    
    #function this
    url = "https://au.wilson.com"
    sitemapURL = url + "/sitemap.xml"
    content = readURL(sitemapURL)
    
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
            #pageChangeFreq = page.get_text().split('\n')[3] #changefreq
            if lastmodFind:
                pageDictionary[pageLastMod] = (pageUrl,imageFindLoc)
            
    print(10*"-","Summary",10*"-")
    recentPages = sorted(pageDictionary.items(), reverse=True)
    for x in range(10):
        print(recentPages[x])
        
#=========MAIN Function=============

if __name__ == '__main__':
    
    watcher = checkLastModified() 

    webCrawl()

