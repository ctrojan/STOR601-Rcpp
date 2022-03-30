# STOR-601 - Interfacing R and C++

Code for the STOR-601 - Interfacing R and C++ assessment. Consists of an [R markdown document](https://htmlpreview.github.io/?https://github.com/ctrojan/STOR601-Rcpp/main/Interfacing-R-and-C%2B%2B---assessment.html) presenting the solutions, alongside the scripts used and their original outputs in csv format.

## Overview

The solutions to all of the tasks in this assessment are presented in [Interfacing-R-and-C++---assessment.html](https://htmlpreview.github.io/?https://github.com/ctrojan/STOR601-Rcpp/main/Interfacing-R-and-C%2B%2B---assessment.html). The R package written for task 1 is hosted in [ctrojan/R/stablemarriageR](https://github.com/ctrojan/STOR601-Rcpp/tree/main/R/stablemarriageR). This repository is organised as follows:

- `/python`
    - `gen_test_tables.py` - the script used to generate the pairs of preference tables for the execution time test
    - `execution_time_test.py` - the script used to time the python implementation on the test tables
    - `/stablemarriagepy` - the python package implementing the stable marriage problem written for the [STOR601 python assessment](https://github.com/ctrojan/STOR601-Python), with some additional functions to save and load preference tables
    - `/results` - containts the results of the python execution time test
    
- `/R`
    - `execution_time_test.R` - the script used to time the Rcpp implementation on the test tables
    - `/stablemarriageR` - the R package implementing the stable marriage problem with Rcpp
    - `/results` - containts the results of the Rcpp execution time test
    
- `/test_tables`
    

## Requirements

The code was written and tested with:

Python
- `python == 3.9.7`

R
- `R == 3.6.3`
    - `devtools == 2.4.3`
    - `Rcpp == 1.0.8`
    - `assertive == 0.3-6`
    
