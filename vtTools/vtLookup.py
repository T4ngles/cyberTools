"""
    VT Rating Request
    To check file hashes against VT database

    [ ]scrape web gui for VT rating
    [ ]obfuscate ip address and agent rotation

"""

import os
import csv

from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import requests

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


def readURL(urlToRead: str):
    if urlToRead == "https://wdt.wilson.com/":
        pass
    else:
        url = urlToRead
        print('url page:' + url)
        req = Request(
            url, 
            #headers={'User-Agent': 'Mozilla/5.0'}
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}            
        )
        content = urlopen(req).read()
        return content

        #content = urllib.request.urlopen(url).read()

def findVTRating(filehash: str):
    # vtFileURL = 'https://www.virustotal.com/gui/file/' + filehash
    # content = readURL(vtFileURL)
    # print(content)
    # soup = BeautifulSoup(content, 'lxml')

    # vtRating = soup.find('div', {"class": "positives"})

    # print(f"File has rating of {vtRating}")

    session = requests.Session()
    session.headers = {'X-Apikey': '<api-key>'}

    sha256Hash = filehash

    url = f"https://www.virustotal.com/api/v3/monitor_partner/hashes/{sha256Hash}/analyses"
    response = session.get(url)
    print(response.text)
    return
        
        
#=========MAIN Function=============

if __name__ == '__main__':
    
    #rating check
    safeTestHash = 'b494d83d2008d6a5e89b60b7a7b1ab55d5f8cbf7471c14b9d7bec6ad77b1bffa'
    maliciousTestHash = '284f083103d1c160d9e4721ecce515646ce451a1b7ddf9dd89817904e21a4a2d'

    findVTRating(maliciousTestHash)

    


