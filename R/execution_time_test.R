#! /usr/bin/env Rscript

# Times the Rcpp implementation of the stable marriage problem fundamental algorithm on the test preference tables

library(stablemarriageR)

filepath <- "../test_tables/"
seed <- 5
reps <- 10
ns <- c(4, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000)

results <- c()
for (n in ns) {
  
  pref1 <- read_pref(paste(filepath,"pref1-seed",seed,"-n",n,".csv", sep=""))
  pref2 <- read_pref(paste(filepath,"pref2-seed",seed,"-n",n,".csv", sep=""))
  
  grp1 <- colnames(pref1)
  grp2 <- colnames(pref2)
  
  times <- c()
  for (rep in 1:reps){
    start <- Sys.time()
    stab <- stablemarriage(grp1, grp2, pref1, pref2, validate_inputs=FALSE)
    end <- Sys.time()
    
    times <- c(times, as.numeric(end - start, units = "secs"))
    print(paste(n, ": ", tail(times, n=1)))
  }
  
  results <- c(results, mean(times))
  print("\n")
}

write.csv(data.frame(n = ns, t = results), "results/execution_time.csv", row.names = FALSE)