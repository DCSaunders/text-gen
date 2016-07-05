#!/usr/bin/env python
import urllib2
import sys
from bs4 import BeautifulSoup

if len(sys.argv)<2:
    exit("Requires full urls, or file path prepended with 'file:'")
else:
    for url in sys.argv[1:]:
        req = urllib2.Request(url)
        try:
            site = urllib2.urlopen(req)
            if url.startswith('file:'):    
                print site.read()
            else:
                site_print = BeautifulSoup(site, 'html.parser')
                print site_print.get_text()
        except Exception as e:
            if hasattr(e, 'reason'):
                print "Failed to reach server: %s" % e.reason
            elif hasattr(e, 'code'):
                print "Error code %s filling request" % e.code
