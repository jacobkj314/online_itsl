class Set:
	def __init__(self, *_set):
		self._set = set(_set)
		self._rehash()

	def _rehash(self):
		self._hash = tuple(sorted(self._set)).__hash__()
	def __hash__(self):
		if self._hash is None:
			self._rehash()
		return self._hash

	def __eq__(self, other):
		return self.__class__ == other.__class__ and self._set == other._set
	def __len__(self):
		return len(self._set)
	def __str__(self):
		return r'{}' if len(self) == 0 else self._set.__str__()
	def __repr__(self):
		return r'{}' if len(self) == 0 else self._set.__repr__()
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

	def add(self, e):
		self._set.add(e)
		self._hash = None
	def update(self, es):
		self._set.update(es)
		self._hash = None
	# I don't think I need methods to remove elements


K = 2

sigma={}
def accept_gold(w, k=K):#This is where I can manually encode a grammar
	return True



from itertools import combinations

def dictUnion(a, b):
	#create a dict and make Sets for each key
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

def f(w, k=K): #get attested factors
	return Set(*(w[i:i+j] for i in range(len(w) - k + 1) for j in range(k+1)))
def x(w, k=K): #get attested augmented subsequences, encoded as a dict from tuples to Sets of Sets
	ansSet = set()
	for j in range(1,k):#iterate across factor lengths
		for xi in list(combinations(range(len(w)), j)):#look at each subsequence of indices
			qi = tuple(map(lambda x : w[x], xi))#look at the symbols at those indices
			ii = Set(*(map(lambda x : w[x], [i for i in range(xi[0],xi[-1]) if i not in xi])))#look at the symbols at the intervening indices
			if len(set(qi).intersection(set(ii))) == 0:#if there is no overlap, it is a valid subsequence
				ansSet.add((qi, ii))
	ansDict = {() : Set(Set())}
	for q, i in ansSet:
		if ansDict.get(q) is None:
			ansDict[q] = Set()
		ansDict[q].add(i)
	return ansDict
def r(asubs): #restrict augmented subsequences
	new = dict()
	for q in asubs:
		i = asubs[q]
		new[q] = Set()

		#this is definitely super inefficient, but I've wasted enough time optimizing already
		for j in i:
			needJ = True
			for k in i:
				if j.issuperset(k) and j != k: #discard strict supersets
					needJ = False
					break
			if needJ:
				new[q].add(j)
	return new


def learn(samples, k=K):
	gl = Set()
	gs = dict()

	for w in samples:
		gl.update(f(w, k=k))
		gs = r(dictUnion(gs, x(w, k=k)))
	return (gl, gs)

def scan(g, w):
	gl, gs = g
	qi = r(dictUnion(gs, x(w)))
	return f(w).issubset(gl) and all(qi[j].issubset(gs[j]) for j in qi)




#This is a dummy TSL-2 grammar for testing
from random import getrandbits, randint
def generate():
	w = ''
	odd = 0; even = 0
	for _ in range(randint(5, 12)):
		incr = randint(0,1)
		if randint(0,1):#even
			if incr and even < 4:
				even += 1
			w += str(even*2)
		else:#odd
			if incr and odd < 4:
				odd += 1
			w += str(odd*2 + 1)
	return w

