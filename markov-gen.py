#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup

class MarkovGen(object):
    def __init__(self, argv):
        for url in argv:
            req = urllib2.Request(url)
            try:
                site = urllib2.urlopen(req)
                if url.startswith('file:'):    
                    print site.read()
                else:
                    site_print = BeautifulSoup(site, 'html.parser')
                    return site_print.get_text()
            except Exception as e:
                if hasattr(e, 'reason'):
                    print "Failed to reach server: %s" % e.reason
                elif hasattr(e, 'code'):
                    print "Error code %s filling request" % e.code
