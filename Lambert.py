'''
This is my scratch paper for testing out ideas from Lambert, D. (2021, August). Grammar interpretations and learning TSL online. In International Conference on Grammatical Inference (pp. 81-91). PMLR.
Retrieved from https://proceedings.mlr.press/v153/lambert21a/lambert21a.pdf
'''

from itertools import combinations, product
from tqdm import tqdm
K = 2; M = 1 #default "hyperparameters" of this implementation. Corresponds to TSL-2 (and possibly MTSL-2 ??)

def nsorted(collection, key = lambda x:x): 
	'''
	This method implements numerical sorting, rather than default lexicographical sorting
	'''
	return sorted(collection, key = lambda element : (len(key(element)), key(element)))

def ordered(d):
	'''
	Like nsorted, but for dictionaries
	'''
	return {k:d[k] for k in nsorted(d)}

def star(sigma, maxLen, filt=lambda *x:True):
	'''
	Given an alphabet sigma (an Iterable), a maximum length, and (optionally) a filter, this method returns every string in that alphabet up to that length that is accepted by the filter 
	'''
	for count in range(maxLen+1):
		for result in filter(filt, (''.join(w) for w in product(*(sigma for _ in range(count))))):
			yield result

class Set:
	'''
	This is just a wrapper class around python's set class, which allows Sets to be placed in other Sets
	'''
	def __init__(self, *_set):
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
		return Set(*(self._set.union(other._set)))

	def add(self, e):
		self._set.add(e)
		self._hash = None; self._ordered = False
	def update(self, es):
		self._set.update(es)
		self._hash = None; self._ordered = False
	# I don't need methods to remove elements




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


#These are the main three algorithms introduced in the paper, adapted to account for ITSL m-width symbols

def f(w, k=K, m=M): 
	'''
	This gets the attested substrings of the m-width symbols within the string w
	'''
	w = itsl(w, m=m)#first break the string into m-width symbols
	return Set(*(w[i:i+j] for j in range(k+1+1) for i in range(len(w) - j + 1))) #first range is 0 to k+1 inclusive, second is from the start of the word to the end

def x(w, k=K, m=M):
	"""
	This function retrieves the set of augmented subsequences and encodes them as a dict from tuples of symbols (subsequeces) to Sets of Sets (the inner sets are the intervener sets, while the outer sets are the sets of intervener sets)
	"""
	w=itsl(w, m=m) #first break the string into m-width symbols
	ansSet = set()
	for j in range(1,k+1):#iterate across factor lengths, 1 to k inclusive
		for xi in list(combinations(range(len(w)), j)):#look at each subsequence of indices
			if True: # # # # # ignoring this condition temporarily # # # # # if all(map(lambda pair: ((diff:=pair[1]-pair[0]) == m or diff >= 2*m), combinations(xi,2))):#only proceed if no pair of selected m-width symbols overlap and leave space for a whole number of interveners
				qi = tuple(map(lambda x : w[x], xi))#look at the symbols at those indices
				ii = Set(*(map(lambda x : w[x], [i for i in range(xi[0],xi[-1]) if all(y != i for y in xi)])))#look at the symbols at the intervening indices
				if len(set(qi).intersection(set(ii))) == 0:#if there is no overlap in terms of selected characters, it is a valid subsequence
					ansSet.add((qi, ii))
	ansDict = {() : Set(Set())}
	for q, i in ansSet:
		if ansDict.get(q) is None:
			ansDict[q] = Set()
		ansDict[q].add(i)
	return ordered(ansDict)

def r(asubs): 
	"""
	this function restricts augmented subsequences, keeping only the smallest ones needed
	"""
	new = dict()
	for q in asubs:
		i = asubs[q]
		new[q] = Set()

		#there is definitely a more efficient way to discard strict supersets
		for j in i:
			needJ = True
			for k in i:
				if j.issuperset(k) and j != k: #discard strict supersets
					needJ = False
					break
			if needJ:
				new[q].add(j)
	return new










def itsl(w, m=M):
	'''
	This breaks the string w into a list of m-width symbols (m is a "hyperparameter" of ITSL/MITSL languages)
	For instance, if 
	m==2, then w=asdfghjkl is represented as the sequence of symbols 'as','sd','df','fg','gh','hj','jk','kl'. If 
	m==3, then it is represented as 								 'asd','sdf','dfg','fgh','ghj','hjk','jkl'
	etc.
	where each of these "m-width symbols" from sigma^m is treated like a singular symbol
	'''
	return tuple([w[i:i+m] for i in range(len(w)-m+1)])
def bound(w,k,m):
	'''
	This adds word boundaries to the string. k*m-1 copies of > before the actual string, and k*m-1 copies of < after the actual string
	The number k*m-1 was chosen so that the earliest possible k-factor of consecutive m-width symbols contains exactly one true symbol from the actual string
	'''
	return '>'*(k*m-1) + w + '<'*(k*m-1)


def grammar(k=K,m=M):
	"""
	Returns a blank grammar (one which rejects every string) that can be used as a starting point for building grammars from positive inputs
	The grammar is a tuple consisting of a Set() (of attested factors) a dict() (representing a set of augmented subsequences) and a tuple of (an int (the tier window width) and an int (the symbol width))
	"""
	return (Set(), dict(), (k,m))
def learn_step(g, w):
	'''
	Given an input grammar g and a string w, performs one online learning step
	'''
	gl, gs, (k,m) = g
	w = bound(w, k,m)
	return (gl.union(f(w, k=k,m=m)), ordered(r(dictUnion(gs, x(w, k=k,m=m)))), (k,m))
def learn(samples, k=None,m=None, g=None):
	'''
	creates a new grammar or takes an existing grammar
	applies learn_step to all strings in samples 
	'''
	k = k if k else (g[2][0] if g else K)
	m = m if m else (g[2][1] if g else M)
	g = g if g else grammar(k,m)
	for w in tqdm(samples, "Learning"):
		g = learn_step(g, w)
	return g
def scan(g, w_raw, verbose=False):
	'''
	given a grammar g and a string w, returns whether the given grammar accepts w
	'''
	gl, gs, (k,m) = g
	w=bound(w_raw,k,m)
	decision = True
	for fgl in f(w, k=k,m=m):
		if fgl not in gl:
			if verbose: 
				print(f"Rejected '{w_raw}', the length-{len(fgl)} substring {fgl} is unattested")
				decision = False # # # # # return False
			else:
				return False
	qi = ordered(r(dictUnion(gs, x(w, k=k,m=m))))
	for j in qi:
		if j not in gs:
			if verbose: 
				print(f"Rejected {w_raw}, the length-{len(j)} subsequence {j} is unattested")
			else:
				return False
			decision = False # # # # # return False
		for qij in qi[j]:
			if (j in gs) and qij not in gs[j]: #added the extra (first) condition to get a full, verbose printout 
				if verbose: 
					print(f"Rejected '{w_raw}', the intervener-set {qij} is not attested or entailed to intervene {j}")
				else:
					return False
				decision = False# # # # # return False
	return decision

def wrong(g, acc, sigstar):
    '''
    This tests a grammar against an acceptor on a list of strings, and returns every string where the grammar gives the 'wrong' answer
    '''
    return [w for w in tqdm(sigstar, "Testing the grammar", ) if scan(g, w) != acc(w)]


import re
def tsl_acceptor(tier, restrictions):
    def acceptor(w, verbose=False):
        w_projected = re.sub(f'[^{"".join(tier)}]', '', '>'+w+'<')
        decision = True
        for restriction in nsorted(restrictions):
            if (r :=''.join(restriction)) in w_projected:
                if verbose:
                    print(f"rejected {w} for containing {r} on tier {tier}: {w_projected}")
                else:
                    return False
                decision = False # # # # # return False
        return decision
    return acceptor
    #return lambda w : not any(''.join(restriction) in re.sub(f'[^{"".join(tier)}]', '', w) for restriction in restrictions) if w is not None else (tier, restrictions)

def mtsl_acceptor(tsl_grammars):
    def acceptor(w, verbose=False):
        if w is None:
            return nsorted([(nsorted(tier), nsorted(restrictions)) for tier, restrictions in tsl_grammars], key= lambda x:x[0])
        decision = True
        for tsl_grammar in nsorted(tsl_grammars, key = lambda x : x[0]):
            if not tsl_acceptor(*tsl_grammar)(w, verbose):
                if not verbose:
                    return False
                decision = False
        return decision
    return acceptor