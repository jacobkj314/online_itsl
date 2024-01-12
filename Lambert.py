#!/usr/bin/env python
# coding: utf-8

# # Python Implementation of online TSL learning algorithm as presented in [Lambert (2021)](https://proceedings.mlr.press/v153/lambert21a/lambert21a.pdf)

# ### imports and definitions

# In[1]:


from itertools import combinations, product
from tqdm import tqdm

# ### Helper Methods

# In[2]:


def nsorted(collection, key = lambda x:x): 
	'''
	This method implements numerical sorting, rather than default lexicographical sorting of sorted()
	'''
	if collection.__class__ == dict:
		return {key:collection[key] for key in nsorted(collection.keys())}
	return sorted(collection, key = lambda element : (len(key(element)), key(element)))

# In[3]:


class Set:
	'''
	This is just a wrapper class around python's set class, which allows Sets to be placed in other Sets
	'''
	def __init__(self, _set = {}):
		self._set = set(_set)
		self._rehash()

	def _rehash(self):
		self._hash = tuple(nsorted(self._set)).__hash__()
	def __hash__(self):
		if self._hash is None:
			self._rehash()
		return self._hash

	def __eq__(self, other):
		return self.__class__ == other.__class__ and self._set == other._set
	def __len__(self):
		return len(self._set)
	def __repr__(self):
		return '{{{0}}}'.format(', '.join(map(repr, nsorted(self._set))))
	def __str__(self):
		return self.__repr__()
	def __lt__(self, other):
		if other.__class__ == self.__class__:
			return self._set.__lt__(other._set)
		return self._set.__lt__(other)
	def __gt__(self, other):
		if other.__class__ == self.__class__:
			return self._set.__gt__(other._set)
		return self._set.__gt__(other)
	def __leq__(self, other):
		if other.__class__ == self.__class__:
			return self._set.__leq__(other._set)
		return self._set.__leq__(other)
	def __geq__(self, other):
		if other.__class__ == self.__class__:
			return self._set.__geq__(other._set)
		return self._set.__geq__(other)
	def __iter__(self):
		return self._set.__iter__()
	def issubset(self, other):
		return self._set.issubset(other._set)
	def issuperset(self, other):
		return self._set.issuperset(other._set)
	def union(self, other):
		return Set((self._set.union(other._set)))
	def difference(self, other):
		return Set(self._set.difference(other._set))

	def add(self, e):
		self._set.add(e)
		self._hash = None; self._ordered = False
	def update(self, es):
		self._set.update(es)
		self._hash = None; self._ordered = False

# In[4]:


def dictUnion(a, b):
	'''
	for sets of augmented subsequences encoded as a dict from tuples of symbols to Sets of Sets, this function unions the two sets
	'''
	ans = dict()
	for e in a:
		ans[e] = Set()
	for e in b:
		ans[e] = Set()
	
	for e in a:
		ans[e].update(a[e])
	for e in b:
		ans[e].update(b[e])
	return ans

# In[5]:


def width_j_substrings(w, j):
    return tuple(w[i:i+j] for i in range(len(w)-j+1))

# In[6]:


class grammar_tuple(tuple):
    '''
    This is just a new definition for __len__ so that the len() of a grammar tuple is meaningful (rather than just always 3)
    '''
    def __len__(self):
        return len(self[1]) + sum(len(item) for item in self[2].values())

# ### Set the standard symbol and dependency widths

# In[7]:


K = 2 # dependency width
M = 2 # symbol width

# ### Learner definitions/prerequisites

# "$ f : \Sigma^* \rightarrow \mathcal{P} \left( \Sigma^{\leq k+1} \right) $
# gathers all and only those substrings of $w$ whose width is bounded above by $ k+1 $"

# In[8]:


def f(w, k=K):
    return Set  (
                    sum (
                            tuple(width_j_substrings(w, j) for j in range(k+1+1)), #get every j-factor for every value of j up to k+1 inclusive
                            ()
                        )
                )

# "$ x : \Sigma^* \rightarrow \mathcal{P} \left( \Sigma^{\leq k} \times \mathcal{P} \left( \Sigma \right) \right) $ extracts the valid augmented subsequences of width bounded above by $k$"

# In[9]:


def x(w, k=K):

    symbols_at_indices = lambda indices : tuple(w[index] for index in indices)
    

    augmented_subsequences = dict()         # Create a dictionary from subsequences to the set of their intervener sets
    augmented_subsequences[()] = Set([Set()]) # The only set of symbols that can intervene a length-0 tuple is the empty set

    for j in range(1, k+1):                                                             # iterate across factor lengths j, 1 to k inclusive
        for subsequence_indices in list(combinations(range(len(w)), j)):                # look at each length-j subsequence of indices
            subsequence = symbols_at_indices(subsequence_indices)               # extract the tuple of symbols at those selected indices
            intervening_indices =   [                                                   # compute the intervening indices
                                        intervening_index
                                        for intervening_index in range(subsequence_indices[0], subsequence_indices[-1])
                                        if intervening_index not in subsequence_indices
                                    ]
            intervening_set = Set(symbols_at_indices(intervening_indices))         # extract the set of symbols at the intervening indices

            if set(subsequence).isdisjoint(set(intervening_set)):           # if there are no symbols shared by the subsequence and the interveners, this is a valid augmented subsequence
                if subsequence not in augmented_subsequences:
                    augmented_subsequences[subsequence] = Set()
                augmented_subsequences[subsequence].add(intervening_set)    # add the set of augmented subsequences

    return nsorted(augmented_subsequences)

# "$ r :  \mathcal{P} \left( \Sigma^{\leq k} \times \mathcal{P} \left( \Sigma \right) \right) \rightarrow \mathcal{P} \left( \Sigma^{\leq k} \times \mathcal{P} \left( \Sigma \right) \right)$ restricts the set of augmented subsequences to exclude any that are entailed by any other"

# In[10]:


def r(augmented_subsequences):
    return  nsorted (
                        {
                            subsequence_symbols: Set((
                                                        intervener_symbol_set
                                                        for intervener_symbol_set in intervener_symbol_sets
                                                        if not any  (
                                                                            intervener_symbol_set.issuperset(other_intervener_symbol_set)
                                                                        and
                                                                            intervener_symbol_set != other_intervener_symbol_set
                                                                        for other_intervener_symbol_set in intervener_symbol_sets
                                                                    )

                                                    ))
                            for subsequence_symbols, intervener_symbol_sets in augmented_subsequences.items()
                        }
                    )

# ### Learners

# "We can define a learner $ \varphi \left( \langle  G_{\ell}, G_s\rangle, w \right) = \langle G_{\ell} \cup f \left( w \right), r \left( G_s \cup x \left( w \right) \right) \rangle$" This is `learn_step`
# 
# "The composite grammar can immediately be used as an acceptor without further processing . . . 
# $ \mathcal{L} \left( \langle G_{\ell}, G_s \rangle \right) = \{ w : f \left( w \right) \subseteq G_{\ell} \land r \left( G_s \cup x \left( w \right) \right) \subseteq G_s \}$
# . In words, a string is accepted iff it has only permitted substrings and each of its valid augmented subsequences is attested or entailed by something that is attested." This is `scan`

# In[11]:


class TSL_Learner:
    def __init__(self, k=K):
        self.k = k          # dependency width
        self.G_l = Set()    # substrings of length bounded above by k+1
        self.G_s = dict()   # augmented subsequences of length bounded above by k
        self._data_source = None
    def __repr__(self):
        return f'TSL-{self.k} Grammar\n{self.G_l}\n{self.G_s}'
    def __call__(self, *args, **kwargs):
        return self.scan(*args, **kwargs)
    def extract_alphabet(self):
        pass # This algorithm does not require this step for learning :)

    @property
    def grammar(self):
        return grammar_tuple((self.k, self.G_l, self.G_s))

    #This is an online algorithm, so it does not need a persistent copy of the strings it sees. To highlight this, I have enforced that the learner ONLY streams inputs from an iterator, without retaining a pointer to the complete input 
    @property
    def data(self):
        return (w for w in [])
    @data.setter
    def data(self, W):
        self._data_source = (w for w in W)


    def preprocess(self, w):
        return '>'*(self.k-1) + w + '<'*(self.k-1) # add word-boundary symbols

    def scan(self, w_raw):
        w = self.preprocess(w_raw)
        return  (
                        f(w, k = self.k).issubset(self.G_l)
                    and
                        all (
                                (
                                        subsequence in self.G_s.keys()
                                    and
                                        intervening_sets.issubset(self.G_s[subsequence])
                                )
                                for subsequence, intervening_sets in r(dictUnion(self.G_s, x(w, self.k))).items()
                            )
                )
    
    def learn_step(self, w_raw):
        w = self.preprocess(w_raw)
        self.G_l = self.G_l.union(f(w, k=self.k))
        self.G_s = r(dictUnion(self.G_s, x(w, self.k)))
    
    def learn(self, W=None):
        W = (w for w in (W if W is not None else self._data_source))
        for w in tqdm(W, desc="Learning"):
            self.learn_step(w)

    def generate_sample(self, n, use_iterator=False):
        def generate_with_iterator(n=n):
            alphabet = set(''.join(''.join(substring) for substring in self.G_l)).difference('<','>')

            j = 0
            while True:
                for w in map(''.join, product(alphabet, repeat=j)):
                    if self.scan(w):
                        yield w
                        n -= 1
                        if n == 0:
                            return
                j += 1
        return ((lambda x:x) if use_iterator else list)(generate_with_iterator())

# In[12]:


class ITSL_Learner(TSL_Learner):
    def __init__(self, k=K, m=M):
        super().__init__(k)
        self.m = m             # symbol width
    def __repr__(self):
        return f'ITSL-({self.k}, {self.m}) Grammar\n{self.G_l}\n{self.G_s}'
    @property
    def grammar(self):
        return grammar_tuple(((self.k, self.m), self.G_l, self.G_s))

    def preprocess(self, w):
        return width_j_substrings( #break string into width-m symbols, i.e. symbols created from m adjacent symbols
            '>'*(self.k*self.m-1) + w + '<'*(self.k*self.m-1), # add word-boundary symbols. Adding k*m-1 ensures that the first k-factor of consecutive m-width symbols contains exactly one true symbol, analogous to adding k-1 word boundary symbols for a TSL learner    
            self.m
        )