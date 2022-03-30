#include<Rcpp.h>
using namespace Rcpp;

#include <iostream>
#include <list>
#include <unordered_map>

typedef std::unordered_map<std::string,std::list<std::string>> pref_table;
typedef std::unordered_map<std::string,std::string> matching_map;


matching_map find_stable_matching(pref_table pref1, pref_table pref2) {
  // Given a pair of preference tables, produces a matching that is stable with respect to the tables. 
  // Implementation of the algorithm described in 'Stable Marriage and Its Relation to Other Combinatorial Problems : 
  // An Introduction to the Mathematical Analysis of Algorithms' by Donald E. Knuth and Martin Goldstein.
  
  // Create imaginary undesirable individual (Omega), add to the end of the rankings in pref2
  std::string Omega = "";
  for (auto& row_a : pref2) {
    row_a.second.push_back(Omega);
  }
  
  // Temporarily partner Omega to the members of group 2
  matching_map matching;
  for (auto& row_a : pref2) {
    matching[row_a.first] = Omega;
  }
  
  // Initialise temporary variables
  std::string A;
  std::string b;
  std::string B;
  
  // Execute fundamental algorithm:
  // iterates over the members of group1 to simulate advances to preferred members of group2,
  // who accept or refuse according to their preferences.
  for (auto& row_A : pref1) {      
    A = row_A.first;
    
    for (;A != Omega;) {
      Rcpp::checkUserInterrupt();
        
      // Look up A's first choice of partner (who has not rejected them yet), b
      b = pref1[A].front();
      
      // Look up b's current partner, B
      B = matching[b];
      
      // Loop over b's preference list, engage to A if A comes before B
      for (auto& suitor_i : pref2[b]) {                
        if (suitor_i == A) {
          matching[b] = A;
          A = B;
          break;
        }
        else if (suitor_i == B) {
          break;
        }  
      }
      
      if (A != Omega) {
        // Whoever was just rejected by b removes b from their preference list
        pref1[A].pop_front();
      }               
    }
  }
  
  return matching;
}


pref_table df_to_pref_table(const Rcpp::DataFrame& df){
  // Convert Rcpp::DataFrame into a preference table
  std::list<std::string> colnames = as<std::list<std::string>>(df.names());
  pref_table pref;
  for(auto& col: colnames){
    pref[col] = as<std::list<std::string>>(df[col]);
  }
  return pref;
}


// [[Rcpp::export]]
Rcpp::List marshall_find_stable_matching(Rcpp::DataFrame df_pref1, Rcpp::DataFrame df_pref2){
  // Take inputs from R and convert to preference tables, return matching to R as a list
  pref_table pref1 = df_to_pref_table(df_pref1);
  pref_table pref2 = df_to_pref_table(df_pref2);
  
  return wrap(find_stable_matching(pref1,pref2));
}