#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
import collections
import re

class MarkovGen(object):
    def get_markov(self):
        return self.markov

    def gen_markov(self):
        allowed =  re.compile(r"^[^<>\(\)/=#{}_[\]+@~`]*$");
        self.markov = dict()
        pref = collections.deque()
        suff = collections.deque()

        for word in self.raw_text.split():
            if allowed.match(word):
                suff.append(word)
                if len(suff)>self.suff_len:
                    pref.append(suff.popleft())
                    if len(pref)>self.pref_len:
                        pref.popleft()
                if len(pref)==self.pref_len and len(suff)==self.suff_len:
                    p = " ".join(pref)
                    s = " ".join(suff)
                    if p in self.markov:
                        self.markov[p].append(s)
                    else:
                        self.markov[p] = [s]
        del self.raw_text
    def __init__(self, url, pref_len, suff_len):
        req = urllib2.Request(url)
        try:
            site = urllib2.urlopen(req)
            if url.startswith('file:'):    
                self.raw_text = site.read()
            else:
                site_print = BeautifulSoup(site, 'html.parser')
                self.raw_text = site_print.get_text()
            self.pref_len = pref_len # overlap between chain links
            self.suff_len = suff_len # length of suffix following from each prefix

            self.gen_markov()
        except Exception as e:
            if hasattr(e, 'reason'):
                print "Failed to reach server: %s" % e.reason
            elif hasattr(e, 'code'):
                print "Error code %s filling request" % e.code
            else:
                print e
