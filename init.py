#!/usr/bin/env python
from MarkovGen import MarkovGen
import sys
import random

if len(sys.argv)<2:
    exit("Requires full urls, or file path prepended with 'file:'")
else:
    for url in sys.argv[1:]:
        pref_len = 1
        suff_len = 3
        num_lines = 100
        min_len = 7
        max_len = 40
        
        mg = MarkovGen(url, pref_len, suff_len)
        d = mg.get_markov()
        for ii in range (0, num_lines):
            starter = random.choice(d.keys())
            line = starter
            sen_len = pref_len
            
            while sen_len < max_len:
                pref = " ".join(line.split()[-pref_len:])
                suff = random.choice(d[pref])
                line += " %s" % suff
                sen_len += suff_len
            print line
