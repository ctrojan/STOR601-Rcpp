#! /usr/bin/env python3

"""
Randomly generates pairs of preference tables of a range of sizes and saves them to csv 
"""

import csv, random, warnings, os
import stablemarriagepy as sm


filepath = "../test_tables/"
seed = 5
ns = [4] + [50] + [ n for n in range(100,1001,100) ] + [ n for n in range(2000,5001,1000) ]

random.seed(seed)
for n in ns :
    grp1, grp2 = ['a' + str(i) for i in range(n)], ['b' + str(i) for i in range(n)]
    stab = sm.stablemarriage(grp1, grp2)

    sm.write_pref(filepath + "pref1-seed%s-n%s.csv"%(seed,n), stab.pref1)
    sm.write_pref(filepath + "pref2-seed%s-n%s.csv"%(seed,n), stab.pref2)