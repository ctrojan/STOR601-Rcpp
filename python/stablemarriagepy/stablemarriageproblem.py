import random, warnings, csv

def write_pref(filename, pref):
    """
    Write preference table to csv.
    
    Parameters
    ----------
    filename : string
        Path to csv file.
    
    pref : dict
        Valid preference table, i.e. dictionary indexed by strings with the values being lists of strings.
    """
    
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(list(pref.keys()))
        writer.writerows(zip(*pref.values()))
            

def read_pref(filename):
    """
    Read preference table from csv.
    
    Parameters
    ----------
    filename : string
        Path to csv file containing preference table.
    
    Returns
    -------
    pref : dict
        Preference table, i.e. dictionary indexed by strings with the values being lists of strings.
        Note: validity is not checked.
    """
    
    pref = {}
    with open(filename, 'r') as csv_file:
        reader = list(csv.DictReader(csv_file))
        
        for col in reader[0].keys():
            pref[col] = []
            
        for row in reader:
            for col in pref.keys():
                pref[col].append(row[col])
                
    return pref


class stablemarriage:
    """
    Class implementing the stable marriage problem as described in: 'Stable Marriage and Its Relation
    to Other Combinatorial Problems : An Introduction to the Mathematical Analysis of Algorithms' 
    by Donald E. Knuth and Martin Goldstein.
    
    
    Attributes
    ----------
    group1 : list
        List of distinct symbols.

    group2 : list
        List of distinct symbols.

    n : int
        Number of individuals in group1 and group2.

    pref1 : dict
        The preferences of group1. Dictionary indexed by symbols in group1, containing lists
        of the individuals in group2, ranked from most to least preferred. 
    
    pref2 : dict
        The preferences of group2. Dictionary indexed by symbols in group2, containing lists
        of the individuals in group1, ranked from most to least preferred.

    matching : dict
        Bijection between group1 and group2. Dictionary indexed by members of group 2,
        containing their partner in group 1.

    score : tuple
        tuple (score1,score2) of the scores of the matching for group1 and group2 respectively.
        Computed as the sum of the rankings of their partners in the corresponding preference table.
        
    """
    
    def __init__(self,group1,group2,pref1=None,pref2=None,matching=None):
        """
        Initialise an instance of the stable marriage problem. If preference tables are not provided,
        preferences are randomised.

        Parameters
        ----------
        group1 : iterable
            List of distinct symbols.

        group2 : iterable
            List of distinct symbols.

        pref1 : dict
            (Optional) Dictionary indexed by symbols in group1, containing lists of the individuals in group2,
            ranked from most to least preferred. 
        
        pref2 : dict
            (Optional) Dictionary indexed by symbols in group2, containing lists of the individuals in group1,
            ranked from most to least preferred.

        matching : dict
            (Optional) Bijection between group1 and group2. Dictionary indexed by members of group 2,
            containing their partner in group 1.        
        """
        
        self.group1 = list(group1)
        self.group2 = list(group2)        
        self.check_valid_groups()
        
        self.n = len(self.group1)
        
        if pref1 or pref2:
            if not pref1 and pref2:
                raise TypeError("Missing argument: preference tables must be provided as a pair")
                
            self.pref1 = pref1
            self.pref2 = pref2            
            self.check_valid_preferences()          
        
        else:
            self.randomise_preferences()
    
        self.matching = matching
        if self.matching:
            self.check_valid_matching(self.matching)
        
        self.score = None
        

    def check_valid_groups(self):
        """
        Check whether group1 and group2 are a valid pair. Raises an error if not.
        """
        if len(self.group1) != len(self.group2):
            raise ValueError("Groups must be of same size")
        
        if len(self.group1) != len(set(self.group1)) or len(self.group2) != len(set(self.group2)):
            raise ValueError("Groups must not contain duplicates")
            
        if '' in self.group1 or '' in self.group2:
            raise ValueError("Group members cannot have name \'\'")
    
    def check_valid_preferences(self):
        """
        Check whether pref1 and pref2 are dictionaries and correspond to each other
        and group1 and group2 in terms of size and content. Raises an error if not.
        """

        if type(self.pref1) != dict or type(self.pref2) != dict:
            raise TypeError("Preference tables must be of type dict")

        # Check that the keys of the tables match group1 and group2.       
        if sorted(list(self.pref1.keys()))!= sorted(self.group1) or sorted(list(self.pref2.keys()))!= sorted(self.group2):
            raise ValueError("Preference tables must match groups")

        # Check if the preferences are lists containing every member of the other group exactly once.
        for i in self.pref1.keys():
            if type(self.pref1[i]) != list:
                raise TypeError("Preferences must be of type list")

            if sorted(self.pref1[i]) != sorted(self.group2):
                raise ValueError("Contents of preference tables must match")

        for j in self.pref2.keys():
            if type(self.pref2[j]) != list:
                raise TypeError("Preferences must be of type list")

            if sorted(self.pref2[j]) != sorted(self.group1):
                raise ValueError("Contents of preference tables must match")
    
    def check_valid_matching(self,matching):
        """
        Check whether the matching is valid and corresponds to group1 and group2.
        Raises an error if not.

        Parameters
        ----------
        matching : dict
            Bijection between group 1 and group 2. Dictionary indexed by members of group 2,
            containing their partner in group 1.
        """
        if type(matching) != dict:
            raise TypeError("Matching must be of type dict")
            
        if sorted(list(matching.keys())) != sorted(self.group2):
            raise ValueError("Keys of matching must be members of group 2")
            
        if sorted(list(matching.values())) != sorted(self.group1):
            raise ValueError("Values of matching must be members of group 1")
  

    def randomise_preferences(self):
        """
        Produces a random pair of preference tables for group1 and group2, stores in pref1 and pref2.
        """
 
        pref1 = {}
        for i in self.group1:
            pref1[i] = random.sample(self.group2,self.n)
        
        self.pref1 = pref1

        pref2 = {}
        for i in self.group2:
            pref2[i] = random.sample(self.group1,self.n) 
        
        self.pref2 = pref2
  

    def check_stability(self,matching=None):
        """
        Tests if a matching is stable with respect to pref1 and pref2.
        If no argument is passed the matching attribute is used.
     
        Parameters
        ----------
        matching : dict
            Bijection between group 1 and group 2. Dictionary indexed by members of group 2,
            containing their partner in group 1.
        
        Returns
        -------
        is_stable : bool
            True if the matching is stable with respect to the tables, False otherwise.
        """
        
        # Check if supplied matching is valid,
        # if no matching supplied use the matching attribute if it exists.        
        if matching == None:
            if self.matching == None:
                raise TypeError("No matching found")
            else:
                matching = self.matching
        else:
            self.check_valid_matching(matching)
        
        inverse_matching = {v: k for k, v in matching.items()}

        # For each member of group2, check if there is a member of group1 who is preferred
        # to their current partner.
        for a in self.group2:
            A = matching[a]
            A_ranking = self.pref2[a].index(A)
            preferred_suitors = self.pref2[a][:A_ranking]

            for B in preferred_suitors:
                b = inverse_matching[B]
                b_ranking = self.pref1[B].index(b)
                a_ranking = self.pref1[B].index(a)

                if a_ranking < b_ranking:
                    return False

        return True        
   

    def find_stable_matching(self,reverse_roles=False):
        """
        Produces a matching that is stable with respect to pref1 and pref2.
     
        Parameters
        ----------
        reverse_roles : bool
            (Optional) Whether to reverse the roles of group1 and group2 in the algorithm.
            Defaults to False.
        
        Returns
        -------
        matching : dict
            Bijection between group1 and group2. Dictionary indexed by members of group2,
            containing their partner in group1.
        """

        # Create temporary copies of pref1 and pref2. 
        # If reverse_roles is True, swap the labelling of the copies.
        if reverse_roles:
            pref2  = {A: prefs[:] for A,prefs in self.pref1.items()}
            pref1  = {a: prefs[:] for a,prefs in self.pref2.items()}
        else:
            pref1  = {A: prefs[:] for A,prefs in self.pref1.items()}
            pref2  = {a: prefs[:] for a,prefs in self.pref2.items()}

        # Create imaginary undesirable individual, add to the end of the rankings in pref2,
        # and temporarily partner them to the members of group2.
        Omega = ''
        suitors = [Omega] + list(pref1.keys())

        for a in pref2.keys():
            pref2[a].append(Omega)
            
        matching = { a: Omega for a in pref2.keys() }

        # Execute fundamental algorithm.
        # Iterates over the members of group1 to simulate advances to preferred members of group2,
        # who accept or refuse according to their preferences.
        k = 0      
        while k < self.n:
            # Call the current suitor A.
            A = suitors[k+1]

            while A != Omega:
                # Look up A's first choice of partner, b.
                b = pref1[A][0]

                # Look up b's rankings of A and their current partner, B.
                A_ranking = pref2[b].index(A)
                B = matching[b]
                B_ranking = pref2[b].index(B)

                # Check if b preferrs A to B.
                if A_ranking < B_ranking:
                    # Partner b with A and repeat procedure with the newly single B.
                    matching[b] = A
                    A = B

                if A != Omega:
                    # b will not accept a proposal from A, so remove b from A's preference list.
                    pref1[A].pop(0)

            k += 1 

        # Return the matching. If reverse_roles=True then return the inverse matching.
        if reverse_roles:
            inverse_matching = {v: k for k, v in matching.items()}
            self.matching = inverse_matching
            return inverse_matching
        else:
            self.matching = matching
            return matching
    
    
    def score_matching(self,matching=None):
        """
        Scores the matching with respect to pref1 and pref2. If no argument is passed the matching
        attribute is used.
     
        Parameters
        ----------      
        matching : dict
            (Optional) Bijection between group1 and group2. Dictionary indexed by members of group2,
            containing their partner in group1.
        
        Returns
        -------
        score1 : int
            The score of the matching for group1. Sum of the rankings of their partners in pref1.

        score2 : int
            The score of the matching for group2. Sum of the rankings of their partners in pref2.
        """

        # Check if supplied matching is valid,
        # if no matching supplied use the matching attribute if it exists.
        if matching == None:
            if self.matching == None:
                raise TypeError("No matching found")
            else:
                matching = self.matching
        else:
            self.check_valid_matching(matching)

        # Warn if the matching is not stable.    
        if not self.check_stability(matching):
            warnings.warn("Matching is not stable.")
            
        score1 = 0
        score2 = 0

        # For each a in group2, look up their partner A.
        # Look up their rankings for each other and add these to score1 and score2.
        for a in self.group2:
            A = matching[a]

            a_ranking = self.pref1[A].index(a)
            score1 += a_ranking

            A_ranking = self.pref2[a].index(A)
            score2 += A_ranking

        # If the score is for the matching attribute, update the score attribute.
        if matching == self.matching:
            self.score = (score1,score2)
        
        return score1, score2