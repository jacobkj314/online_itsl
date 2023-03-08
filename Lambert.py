'''
This is just my scratch paper for testing out ideas from Lambert, D. (2021, August). Grammar interpretations and learning TSL online. In International Conference on Grammatical Inference (pp. 81-91). PMLR.
Retrieved from https://proceedings.mlr.press/v153/lambert21a/lambert21a.pdf
'''

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
	def union(self, other):
		return Set(*(self._set.union(other._set)))

	def add(self, e):
		self._set.add(e)
		self._hash = None
	def update(self, es):
		self._set.update(es)
		self._hash = None
	# I don't need methods to remove elements


K = 2

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
	return Set(*(w[i:i+j] for j in range(k+1+1) for i in range(len(w) - j + 1))) #first range is 0 to k+1 inclusive, second is from the start of the word to the end
def x(w, k=K): #get attested augmented subsequences, encoded as a dict from tuples to Sets of Sets
	ansSet = set()
	for j in range(1,k+1):#iterate across factor lengths - 1 to k inclusive
		for xi in list(combinations(range(len(w)), j)):#look at each subsequence of indices
			qi = tuple(map(lambda x : w[x], xi))#look at the symbols at those indices
			ii = Set(*(map(lambda x : w[x], [i for i in range(xi[0],xi[-1]) if i not in xi])))#look at the symbols at the intervening indices
			if len(set(qi).intersection(set(ii))) == 0:#if there is no overlap in terms of selected characters, it is a valid subsequence
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

def grammar(k=K):
	return (Set(), dict(), k)
def learn_step(g, w):
	gl, gs, k = g
	return (gl.union(f(w, k=k)), r(dictUnion(gs, x(w, k=k))), k)
def learn(samples, k=K):
	g = grammar(k)
	for w in samples:
		g = learn_step(g, w)
	return g
def scan(g, w):
	gl, gs, k = g
	qi = r(dictUnion(gs, x(w, k=k)))
	return f(w, k=k).issubset(gl) and all(((j in gs) and (qi[j].issubset(gs[j]))) for j in qi)


#This is a dummy TSL-2 grammar for testing
#the tier consists of odd digits, which cannot "decrease" through the word. So 11111, 33333, 99999, are all ok, 13339 is ok, but 75 is NOT
from random import randint
def generate():
	w = ''
	odd = 0
	for _ in range(randint(5, 12)):
		incr = randint(0,1)
		if randint(0,1):#even
			w += str(randint(0,4)*2)
		else:#odd
			if incr and odd < 4:
				odd += 1
			w += str(odd*2 + 1)
	return w
def accept(w):
	odd = 1; even = 0
	for s in w:
		s = int(s)

		if s % 2 == 1:
			if s < odd:
				return False
			odd = s
		else:
			continue
	return True



#This is a dummy MTSL-2 grammar for testing
#It has a second tier consisting of even digits with the same property as above, so 00000, 44444, 88888 are ok, as is 02468, but 20 is NOT ok.
from random import randint
def generate_mtsl():
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
def accept_mtsl(w):
	odd = 1; even = 0
	for s in w:
		s = int(s)

		if s % 2 == 1:
			if s < odd:
				return False
			odd = s
		else:
			if s < even:
				return False
			even = s
	return True

#This is another, more complicated dummy MTSL-2 grammar for testing
#This grammar adds a 3rd tier, consisting of 0369, which also must occur in "increasing" order 
from random import randint
def generate_mtsl_b():
	w = ''
	odd = 0; even = 0; three = 0
	for _ in range(randint(5, 12)):
		incr = randint(0,1)
		if randint(0,1):#even
			if incr and even < 4:
				even += 1
			next = even*2
		else:#odd
			if incr and odd < 4:
				odd += 1
			next = odd*2 + 1
		if next%3 == 0:
			if next < three:
				if next%2 == 0:
					if even < 4:
						even += 1
				else:
					if odd < 4:
						odd += 1
				continue
			three = next
		w += str(next)
	return w
def accept_mtsl_b(w):
	odd = 1; even = 0; three = 0
	for s in w: #check even and odd requirements
		s = int(s)

		if s % 2 == 1:
			if s < odd:
				return False
			odd = s
		else:
			if s < even:
				return False
			even = s
	for s in w: #check three requirements
		s = int(s)
		if s % 3 == 0:
			if s < three:
				return False
			three = s
	return True

#This is the example from the original paper!
sample = ['akkalkak','klark','kralk','karlakalra','akrala','aklara','rakklarkka','arkralkla','laarlraalr','kaaakkrka','klkkklrk','krlkrkl','alrla']

#this is a mtsl example adapted from the original paper's example
import re
sample2 = sample + [re.sub('a', 'e', w) for w in sample] #replace all as with es and also add them to the sample, so now there is a second tier with a vowel harmony