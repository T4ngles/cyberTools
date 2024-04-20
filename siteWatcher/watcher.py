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
import csv

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

def webCrawl(urlToCrawl: str, domainBound: str):
    #create dictionary of web links and if visited and visit time.

    #urlToCrawl = "https://www.tennisonly.com.au/Wilson_Tennis_Racquets.html"
    #domainBound = "https://www.tennisonly.com.au"
    
    linkSet = set()

    foundLinks = findLinks(urlToCrawl, linkSet, "1", domainBound)
    
    for link in foundLinks:
        newLinks = findLinks(link, linkSet, "2", domainBound)
    
    return linkSet


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
            debugPrint(f"checking link {link}")
            try:
                if ("https://" in link['href'] or "http://" in link['href']) and link['href'][-5:] == '.html':
                    newLink = link['href']
                    #need to refactor and functionise these checks
                    if newLink in linkSet:
                        pass
                    else:
                        linkSet.add(newLink)
                        links.append(newLink)
                        print(" "*4, newLink)

                elif link['href'][-5:] == '.html':
                    debugPrint(f".html found but no http in {link['href']}")
                    if link['href'][0] == "/":            
                        newLink = siteDomain + link['href']
                    elif "../" in link['href'][0]:
                        newLink = urlToSearch + link['href']
                    else:
                        newLink = siteDomain + "/" + link['href']

                    if newLink in linkSet:
                        pass
                    else:
                        linkSet.add(newLink)
                        links.append(newLink)
                        print(" "*4, newLink)
                else:
                    pass
            except TypeError as e:
                print(link,f"has error of {e}")
            
            

        print(f"Round {roundTag}: linkset size is {len(linkSet)}")
        return links
    
    except HTTPError or URLError as e:
        print(e,urlToSearch)


def checkLastModified(url):
    print("#"*20)
    print("Check started at:" + str(datetime.now().time()))
    
    #function this
    #url = "https://au.wilson.com"
    #url = "https://www.tennisonly.com.au"
    sitemapURL = url + "/sitemap.xml"
    content = readURL(sitemapURL)
    
    xmlSoup = BeautifulSoup(content, 'xml') #xml is the default xml parser can check for new ones
        
    siteXMLs = []
    pageDictionary = {}
    
    for xmlURL in xmlSoup.find_all('loc'):
        siteXMLs.append(xmlURL.get_text())
                
    debugPrint(siteXMLs)

    for xmlURL in siteXMLs:
        debugPrint(xmlURL)
        #try here to catch 404's
        if "http" == xmlURL[0:4]:
            debugPrint("is a direct link")
        else:
            xmlURL = url+xmlURL
            debugPrint(f"is a relative link. Changing item to: {xmlURL}")
        try:
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
        except HTTPError as e:
            print(f"{e}")
            
    print(10*"-","Summary",10*"-")
    print(pageDictionary.items())
    recentPages = sorted(pageDictionary.items(), reverse=True)
    for x in range(10):
        print(recentPages[x])

def findTableData(urlToSearch: str):
    try:
        content = readURL(urlToSearch)
        soup = BeautifulSoup(content, 'lxml')

        #racquet dict
        racquetDict = {}
        #is racquet page


        #is not racquet page

        racquetName = soup.find('title').text[:-14]
        print(racquetName)
        racquetDict["racquetName"] = racquetName

        try:
            racquetPrice = soup.find('div', {"class": "desc_top gtm_detail"})['data-gtm_detail_price']
            racquetDict["racquetPrice"] = racquetPrice
            
            #find specs table
            for productSpecsTable in soup.find_all('div', {'id': 'product_specs'}):
                
                #go through spec rows
                for row in productSpecsTable.find_all('tr'):
                    
                    #pull out spec keys and values
                    try:
                        #use strong tags to find heading
                        rowKey = row.find('strong').text.strip(":")
                        if rowKey == "String Pattern":
                            continue
                        rowValue = row.find('strong').next_sibling.text.strip()
                        if rowValue == "":  #sometimes <span> tag is placed to space out values this checks and skips the span value
                            rowValue = row.find('strong').next_sibling.next_sibling.text.strip()

                        racquetDict[rowKey] = rowValue
                    except AttributeError as e:
                        #sometimes strong tag is not used instead bold is used so next_element method is used as fallback
                        print(f"error finding strong {e}")
                        try:
                            rowKey = row.next_element.text.strip(":")
                            if rowKey == "String Pattern":
                                continue
                            rowValue = row.next_element.next_sibling.text.strip()
                            racquetDict[rowKey] = rowValue
                        except AttributeError as e:
                            print("no strong and cannot use next element and sibling")
                            pass

                        

            print(f"Racquet specs for {racquetName} found")
            print(racquetDict)
            return racquetDict
        
        except TypeError as e:
            print(f'not racquet page? {e}')
            return None
    
    except HTTPError or URLError as e:
        print(e,urlToSearch)
        return None

def getRacquetData(masterLinkSet):
    masterRacquetDict = {}

    for link in masterLinkSet:

        racquetDict = findTableData(link)

        if racquetDict:        
            masterRacquetDict[racquetDict['racquetName']] = racquetDict
        
        #findTableData("https://www.tennisonly.com.au/Prince_Phantom_100G/descpage-PTXP1G.html")
    
    racquetListName = 'Tennis Only Racquets.csv'

    fieldnames = ['racquetName',
                  'racquetPrice',
                  'Head Size',
                  'Length',
                  'Strung Weight',
                  'Balance',
                  'Swingweight',
                  'Stiffness',
                  'Beam Width',
                  'Composition',
                  'Power Level',
                  'Stroke Style',
                  'Swing Speed',
                  'Racquet Colors',
                  'Grip Type',
                  'String Pattern',
                  'String Tension'
                  ]

    with open(racquetListName, 'w', encoding='utf-8', newline='') as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        print("Racquet Table")

        for racquet in masterRacquetDict.values():
            
            print(racquet["racquetName"] + "    " + racquet["racquetPrice"])
            writer.writerow(racquet)
        
#=========MAIN Function=============

if __name__ == '__main__':
    
    #watcher = checkLastModified("https://au.wilson.com") #https://au.wilson.com #https://www.tennisonly.com.au
    # domain = "https://www.tennisonly.com.au"
    # pagesToCrawl = [
    #     "https://www.tennisonly.com.au/Wilson_Tennis_Racquets.html",
    #     "https://www.tennisonly.com.au/Babolat_Tennis_Racquets.html",
    #     "https://www.tennisonly.com.au/Head_Tennis_Racquets.html",
    #     "https://www.tennisonly.com.au/Prince_Tennis_Racquets.html",
    #     "https://www.tennisonly.com.au/Yonex_Tennis_Racquets.html",
    #     "https://www.tennisonly.com.au/Volkl_Tennis_Racquets.html",
    #     "https://www.tennisonly.com.au/Dunlop_Tennis_Racquets.html",
    #     "https://www.tennisonly.com.au/Gamma_Tennis_Racquets.html",
    #     "https://www.tennisonly.com.au/Solinco_Tennis_Racquets/catpage-STR.html",
    #     "https://www.tennisonly.com.au/Tecnifibre_Tennis_Racquets.html",
    # ]

    domain = "https://patrickrothfuss.com"
    pagesToCrawl = [
        "https://patrickrothfuss.com"
    ]
    
    masterLinkSet = set()

    for page in pagesToCrawl:
        masterLinkSet.update(webCrawl(page,domain))

    for item in masterLinkSet:
        print(item)

    #getRacquetData(masterLinkSet)
    


