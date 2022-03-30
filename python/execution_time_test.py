#! /usr/bin/env python3

"""
Times the python implementation of the stable marriage problem fundamental algorithm on the test preference tables
"""

import csv, random, warnings, time
import stablemarriagepy as sm


filepath = "../test_tables/"
seed = 5
reps = 10
ns = [4] + [50] + [ n for n in range(100,1001,100) ] + [ n for n in range(2000,5001,1000) ]

results = []

for n in ns :
    pref1 = sm.read_pref(filepath + "pref1-seed%s-n%s.csv"%(seed,n))
    pref2 = sm.read_pref(filepath + "pref2-seed%s-n%s.csv"%(seed,n))
    
    grp1 = list(pref1.keys())
    grp2 = list(pref2.keys())
    
    stab = sm.stablemarriage(grp1, grp2, pref1, pref2)
    
    times = []
    
    for rep in range(reps):
        start = time.perf_counter()
        stab.find_stable_matching()    
        end = time.perf_counter()
        
        times.append(end - start)
        print("%s: %s"%(n, end - start))
    
    results.append(sum(times)/reps)
    print("\n") 
    
    
with open("results/execution_time.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["n","t"])
    writer.writerows(zip(ns,results))