
#' Read in a preference table
#' 
#' @name read_pref
#'
#' @description This is a convenience wrapper for \code{read.csv} with \code{stringsAsFactors = FALSE} .
#'
#' @param file the name of the file containing the preference table
#' 
#' @return A \code{data.frame} containing the data in the file
#' 
#' @export
read_pref <- function(file) {
  read.csv(file, stringsAsFactors = FALSE)
}



#' Check whether a pair of groups is valid
#' 
#' @name check_valid_groups
#' 
#' @description Raises an error if the inputs are not a valid pair of groups.
#' 
check_valid_groups <- function(group1, group2) {
  
  assert_is_character(group1)
  assert_is_character(group2)
  
  assert_all_are_non_missing_nor_empty_character(group1)
  assert_all_are_non_missing_nor_empty_character(group2)
  
  assert_are_same_length(group1, group2)
}



#' Check whether a pair of preference tables is valid
#' 
#' @name check_valid_preferences
#' 
#' @description Checks whether pref1 and pref2 are data frames that correspond to each other 
#' and groups 1 & 2 in terms of size and content, raises an error otherwise.
#' 
check_valid_preferences <- function(group1, group2, pref1, pref2) {

  assert_is_data.frame(pref1)
  assert_is_data.frame(pref2)
  
  assert_have_same_dims(pref1, pref2)
  
  assert_are_set_equal(group1, colnames(pref1))
  assert_are_set_equal(group2, colnames(pref2))
  
  for (col in 1:ncol(pref1)) {
    assert_are_set_equal(pref1[,col], group2)
    assert_are_set_equal(pref2[,col], group1)
  }
}



#' Generate a random pair of preference tables
#' 
#' @name randomise_preferences
#' 
#' @description Produces a random pair of preference tables for group1 and group2
#' 
#' @param group1 character vector of distinct nonempty strings
#' @param group2 character vector of distinct nonempty strings
#' 
#' @return Returns a list containing the two preference tables .
#' 
#' @example 
#' \code{
#' group1 <- c("A", "B", "C", "D")
#' group2 <- c("a", "b", "c", "d")
#' 
#' prefs <- randomise_preferences(group1, group2)
#' prefs$pref1
#' prefs$pref2
#' }
#' 
#' @export
randomise_preferences <- function(group1, group2) {
  n = length(group1)
  
  pref1 <- data.frame( stringsAsFactors = FALSE)
  pref1[1:n,] <- ""
  for (i in 1:n) {
    pref1[,i] <- sample(group2, n)
  }
  colnames(pref1) <- group1
  
  pref2 <- data.frame( stringsAsFactors = FALSE)
  pref2[1:n,] <- ""
  for (i in 1:n) {
    pref2[,i] <- sample(group1, n)
  }
  colnames(pref2) <- group2
  
  
  return(list("pref1"=pref1, "pref2"=pref2))
}



#' An S4 class to represent an instance of the stable marriage problem
#' 
#' @name stablemarriageclass
#' 
#' @description 
#' 
#' @slot group1 character vector of distinct nonempty strings.
#' @slot group2 character vector of distinct nonempty strings.
#' @slot pref1 data frame with a column for each member of \code{group1} 
#'   containing the members of \code{group2} sorted from most to least preferred.
#' @slot pref2 data frame with a column for each member of \code{group2} 
#'   containing the members of \code{group1} sorted from most to least preferred.
#' @slot matching data frame with members of \code{group2} as column names containing 
#'   a bijection between \code{group2} and \code{group1}.
#'   
#' @seealso \code{\link{stablemarriage}}
#'   
#' @export
setClass("stablemarriageclass", 
         representation(group1="character", group2="character", pref1="data.frame", pref2="data.frame", matching="data.frame"))



#' Displays instances of S4 objects of type \code{\link{stablemarriageclass}}
#' 
#' @name show
#' 
#' @description Displays the groups and their preference tables, as well as a
#'   matching if found
#'   
#' @param object An instance of an S4 object of type \code{\link{stablemarriageclass}}.
#' 
#' @seealso \code{\link{stablemarriageclass}}
#' 
#' @export
setMethod("show", "stablemarriageclass",
          function(object) {
            cat("Instance of the stable marriage problem.\n\n")
            
            cat("Group 1 members: ", object@group1, "\n")
            cat("Preferences of group 1:\n")
            print(object@pref1)
            cat("\n")
            
            cat("Group 2 members: ", object@group2, "\n")
            cat("Preferences of group 2:\n")
            print(object@pref2)
            cat("\n")
            
            if (length(object@matching) > 0) {
              cat("Stable matching:\n")
              print(object@matching)
            }
            else {
              cat("Stable matching: not yet found.")
            }

          }
)



#' Solves instances of the stable marriage problem
#' 
#' @name stablemarriage
#' 
#' @description Solves instances of the stable marriage problem as described in: 
#'   'Stable Marriage and Its Relation to Other Combinatorial Problems : 
#'   An Introduction to the Mathematical Analysis of Algorithms' 
#'   by Donald E. Knuth and Martin Goldstein.
#'   
#' @param group1 character vector of distinct nonempty strings.
#' @param group2 character vector of distinct nonempty strings.
#' @param pref1 data frame with a column for each member of \code{group1} 
#'   containing the members of \code{group2} sorted from most to least preferred. 
#'   Optional - if not supplied preference tables will be randomised.
#' @param pref2 data frame with a column for each member of \code{group2} 
#'   containing the members of \code{group1} sorted from most to least preferred.
#'   Optional - if not supplied preference tables will be randomised.
#' @param validate_inputs logical value (default: \code{TRUE}) indicating whether
#'   to check that the groups and preference tables supplied are valid.
#'   
#' @return An instance of an S4 object of type \code{\link{stablemarriageclass}}, 
#'   containing a stable matching for the problem.
#'
#' @seealso \code{\link{stablemarriageclass}}, \code{\link{randomise_preferences}}
#' 
#' @export
stablemarriage <- function(group1, group2, pref1=NULL, pref2=NULL, validate_inputs = TRUE) {

  if (validate_inputs) {
    check_valid_groups(group1, group2)  

    if (!is.null(pref1) || !is.null(pref2)) {
      if (is.null(pref1) || is.null(pref2)) {
        # Throw error if only one preference table is supplied
        stop("missing argument - preference tables must be provided as a pair")
      }
      else {
        # If both pref1 and pref2 are supplied: 
        # convert any factor columns to character and check if tables are valid
        if (TRUE %in% sapply(pref1, is.factor)) {
          pref1 <- rapply(pref1, as.character, classes="factor", how="replace")
        }
        if (TRUE %in% sapply(pref2, is.factor)) {
          pref2 <- rapply(pref2, as.character, classes="factor", how="replace")
        }
  
        check_valid_preferences(group1, group2, pref1, pref2)     
      }
  }
    else {
      # If pref1 and pref2 are not supplied, generate random preference tables
      prefs <- randomise_preferences(group1, group2)
      pref1 <- prefs$pref1
      pref2 <- prefs$pref2
    }
  }
  
  # find a stable matching, convert to dataframe and sort columns according to the order in pref2
  matching <- data.frame(marshall_find_stable_matching(pref1,pref2), stringsAsFactors = FALSE)[colnames(pref2)]
  
  return(new("stablemarriageclass", group1=group1, group2=group2, pref1=pref1, pref2=pref2, matching=matching))
}

