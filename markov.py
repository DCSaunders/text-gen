#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys
import random
import urllib2
import collections
import re

class MarkovGen(object):
    # Return the markov chain dictionary
    def get_markov(self):
        return self.markov
    
    def gen_markov(self):
        allowed =  re.compile(r"^[^<>\(\)/=#{}_[\]+@~`]*$")
        pref = collections.deque()
        suff = collections.deque()
    
        for word in self.raw_text.split():
            # Avoid strange characters from html etc
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
                        self.markov[p][s] += 1
                    else:
                        self.markov[p] = collections.defaultdict(int, [(s,1)])
        del self.raw_text # save memory

    # Reads source file and requested prefix/suffix length
    def __init__(self, url, pref_len, suff_len, lower):
        req = urllib2.Request(url)
        self.markov = {}
        try:
            site = urllib2.urlopen(req)
            if url.startswith('file:'):    
                self.raw_text = site.read()
            else:
                site_print = BeautifulSoup(site, 'html.parser')
                self.raw_text = site_print.get_text()
            if lower:
                self.raw_text = self.raw_text.lower()
            self.pref_len = pref_len # overlap between chain links
            self.suff_len = suff_len # length of suffix following each prefix

            self.gen_markov()
        except Exception as e:
            if hasattr(e, 'reason'):
                print "Failed to reach server: %s" % e.reason
            elif hasattr(e, 'code'):
                print "Error code %s filling request" % e.code
            else:
                print e

# Pick a suffix at random from weighted dictionary        
def dictPick(d):
    r = random.uniform(0, sum(d.itervalues()))
    s = 0
    for k, w in d.iteritems():
        s += w
        if r < s:
            break
    return k

def main():
    if len(sys.argv)<2:
        exit("Needs file path prepended with 'file:', e.g. file:Documents/fic.txt")
    else:
        for url in sys.argv[1:]:
            pref_len = 2
            suff_len = 1
            num_lines = 50
            min_len = 7
            max_len = 50
            lower = True
            
            mg = MarkovGen(url, pref_len, suff_len, lower)
            
            d = mg.get_markov()
            for ii in range (0, num_lines):
                starter = random.choice(d.keys())
                line = starter
                sen_len = pref_len
                while sen_len < max_len:
                    pref = " ".join(line.split()[-pref_len:])
                    suff = dictPick(d[pref])
                    line += " %s" % suff
                    sen_len += suff_len
                print line

if __name__ == '__main__':
    main()
