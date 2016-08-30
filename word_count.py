#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys
import random
import urllib2
import collections
import re

class WordCounter(object):
    def __init__(self, url):
        req = urllib2.Request(url)
        try:
            site = urllib2.urlopen(req)
            if url.startswith('file:'):    
                self.raw_text = site.read()
            else:
                site_print = BeautifulSoup(site, 'html.parser')
                # should see if reading lines is possible with BS and definitely if a file - this will break for big files
                self.raw_text = site_print.get_text()
            for word in self.raw_text.split():
                print word
                
        except Exception as e:
            if hasattr(e, 'reason'):
                print "Failed to reach server: %s" % e.reason
            elif hasattr(e, 'code'):
                print "Error code %s filling request" % e.code
            else:
                print e

def main():
    if len(sys.argv)<2:
        exit("Needs path prepended with 'file:', e.g. file:Documents/fic.txt")
    else:
        for url in sys.argv[1:]:
            wc = WordCounter(url)

            
if __name__ == '__main__':
    main()
