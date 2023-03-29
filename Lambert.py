'''
This is just my scratch paper for testing out ideas from Lambert, D. (2021, August). Grammar interpretations and learning TSL online. In International Conference on Grammatical Inference (pp. 81-91). PMLR.
Retrieved from https://proceedings.mlr.press/v153/lambert21a/lambert21a.pdf
'''

def nsorted(collection): #implement numerical sorting, rather than default lexicographical sorting
	return sorted(collection, key = lambda element : (len(element), element))

def star(sigma, maxLen, filt=lambda *x:True):
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
		self._ordered = False; self._order()

	def _rehash(self):
		self._hash = tuple(nsorted(self._set)).__hash__()
	def __hash__(self):
		if self._hash is None:
			self._rehash()
		return self._hash
	
	def _order(self):
		if not self._ordered:
			self._set = {e for e in nsorted(self._set)}
			self._ordered = True

	def __eq__(self, other):
		return self.__class__ == other.__class__ and self._set == other._set
	def __len__(self):
		return len(self._set)
	def __repr__(self):
		self._order()
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

def ordered(d):
	return {k:d[k] for k in nsorted(d)}

K = 2; M = 1

from itertools import combinations

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

def f(w, k=K, m=M): #get attested factors
	w = itsl(w, m=m)
	return Set(*(w[i:i+j] for j in range(k+1+1) for i in range(len(w) - j + 1))) #first range is 0 to k+1 inclusive, second is from the start of the word to the end
'''def f(w, k=K, m=M): #get attested factors
	w = itsl(w, m=m)# # # # # Added new *m:m to skip ahead, ignoring overlaps
	return Set(*(w[i:i+j*m:m] for j in range(k+1+1) for i in range(len(w) - j + 1))) #first range is 0 to k+1 inclusive, second is from the start of the word to the end
	# # # # #return Set(*(w[i:i+j] for j in range(k+1+1) for i in range(len(w) - j + 1))) #first range is 0 to k+1 inclusive, second is from the start of the word to the end
'''
def x(w, k=K, m=M): #get attested augmented subsequences, encoded as a dict from tuples to Sets of Sets
	"""
	This function retrieves the set of augmented subsequences and encodes them as a dict from tuples of symbols (subsequeces) to Sets of Sets (the inner sets are the intervener sets, while the outer sets are the sets of intervener sets)
	"""

	w=itsl(w, m=m) #first break the string into m-width symbols
	ansSet = set()
	for j in range(1,k+1):#iterate across factor lengths, 1 to k inclusive
		for xi in list(combinations(range(len(w)), j)):#look at each subsequence of indices
			if all(map(lambda pair: ((diff:=pair[1]-pair[0]) == m or diff >= 2*m), combinations(xi,2))):#only proceed if no pair of selected m-width symbols overlap and leave space for a whole number of interveners
				qi = tuple(map(lambda x : w[x], xi))#look at the symbols at those indices
				ii = Set(*(map(lambda x : w[x], [i for i in range(xi[0],xi[-1]) if all(abs(y-i) >=m for y in xi)])))#look at the symbols at the intervening and non-overlapping indices
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
	return tuple([w[i:i+m] for i in range(len(w)-m+1)])
def bound(w,k,m):
	return '>'*(k*m-1) + w + '<'*(k*m-1)


def grammar(k=K,m=M):
	"""
	Returns a blank grammar (rejecting every string) that can be used as a starting point for building grammars from input
	The grammar consists of a Set() (of attested factors) a dict() (representing a set of augmented subsequences) and an int (the tier window width)
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
	for w in samples:
		g = learn_step(g, w)
	return g
def scan(g, w):
	'''
	given a grammar g and a string w, returns whether the given grammar accepts w
	'''
	gl, gs, (k,m) = g
	w=bound(w,k,m)
	qi = r(dictUnion(gs, x(w, k=k,m=m)))
	return f(w, k=k,m=m).issubset(gl) and all(((j in gs) and (qi[j].issubset(gs[j]))) for j in qi)


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




surface = {(0,0):'S',(0,1):'s',(1,0):'Z',(1,1):'z',}
underlying = {surface[f]:f for f in surface}
def generate_mtsl_blockers():
	w = ''
	voice = randint(0,1); anterior = None
	for _ in range(randint(5, 12)):
		if randint(1,3) == 1:
			w += 't'
			anterior = None
			continue
		if anterior is None:
			anterior = randint(0,1)
		w += surface[(voice, anterior)]
	return w
def accept_mtsl_blockers(w):
	voicing = [underlying[s][0] for s in w if s != 't']
	if not all(s == voicing[0] for s in voicing):
		return False
	for blocked in w.split('t'):
		anteriority = [underlying[s][0] for s in blocked]
		if not all(s == anteriority[0] for s in anteriority):
			return False
	return True


def generate_itsl():
	c = 'd' if randint(0,1) else 'n'
	w = ''
	for _ in range(randint(5,12)):
		if randint(1,2) == 1:
			if randint(1,2) == 1:
				w += 'nd'
			else:
				w += c
		else:
			w += 'x'
	return w
def accept_itsl(w):
	w = re.sub('nd','',w)
	w = re.sub('x','',w)
	return w in [x * len(w) for x in ('n','d')]

#This is supposed to help automate testing
pointers = []
from itertools import product
def failures(accept, sigma, count=None, k=K, m=M):
	count = count if count else (k+1)*(m+1)
	sigmastar = star(sigma, (k+1)*(m+1))
	sample = list(filter(lambda *x: accept(*x), sigmastar))
	sample = ['>'+w+'<' for w in sample]
	g = learn(sample, k=k,m=m)
	pointers.clear()
	pointers.extend([sigmastar, sample, g])
	return [(w, a, t) for w in star(sigma, count) if ((a := accept(w)) != (t:= scan(g,'>'+w+'<')))]

#it is still failing on itsl, I haven't figured out how to ignore overlapping m-width symbols yet...
rejects = failures(accept_itsl, 'nd',k=2,m=2)



sh = ['SaSekuS', 'sasokos', 'SakuSuS', 'sakesas',
'SeSukuS', 'sesukos', 'SekeSuS', 'sekoses',
'SiSokeS', 'sisekos', 'SikiSoS', 'sikisis',
'SoSokeS', 'sosakos', 'SokaSeS', 'sokusas',
'SuSakiS', 'susukos', 'SukoSoS', 'sukasus',
'SaSokuS', 'sasakus', 'SakuSiS', 'sakisos',
'SeSokiS', 'sesukis', 'SekeSoS', 'sekeses',
'SiSukoS', 'sisokos', 'SikeSaS', 'sikasos',
'SoSokuS', 'sosikas', 'SokeSiS', 'sokosis',
'SuSakeS', 'susokis', 'SukoSeS', 'sukesas']

fl = ['SasokuS', 'saSakus', 'SaSekuS', 'sasokos',
'SesokiS', 'seSukis', 'SeSukuS', 'sesukos',
'SisukoS', 'siSokos', 'SiSokeS', 'sisekos',
'SosokuS', 'soSikas', 'SoSokeS', 'sosakos',
'SusakeS', 'suSokis', 'SuSakiS', 'susukos',
'SakusiS', 'sakiSos', 'SakuSuS', 'sakesas',
'SekesoS', 'sekeSes', 'SekeSuS', 'sekoses',
'SikesaS', 'sikaSos', 'SikiSoS', 'sikisis',
'SokesiS', 'sokoSis', 'SokaSeS', 'sokusas',
'SukoseS', 'sukeSas', 'SukoSoS', 'sukasus']

ifl = ['SasokuS', 'saSakus', 'SakusiS', 'sakiSos',
'SesokiS', 'seSukis', 'SekesoS', 'sekeSes',
'SisukoS', 'siSokos', 'SikesaS', 'sikaSos',
'SosokuS', 'soSikas', 'SokesiS', 'sokoSis',
'SusakeS', 'suSokis', 'SukoseS', 'sukeSas',
'SasekuS', 'saSokos', 'SakusuS', 'sakeSas',
'SesukuS', 'seSukos', 'SekesuS', 'sekoSes',
'SisokeS', 'siSekos', 'SikisoS', 'sikiSis',
'SosokeS', 'soSakos', 'SokaseS', 'sokuSas',
'SusakiS', 'suSukos', 'SukosoS', 'sukaSus']

test = ['sekoSos', 'SekoSos', 'sukisas', 'sukisaS', 'SoSukoS', 'SosukoS',
'SasokaS', 'Sasokas', 'SeSekaS', 'seSekaS', 'sukesus', 'sukeSus',
'suSekos', 'suSekoS', 'SokuSiS', 'SokuSis', 'sisakus', 'siSakus',
'SikisaS', 'sikisaS', 'sisokus', 'Sisokus', 'SakaSoS', 'SakasoS',
'seSokos', 'seSokoS', 'SekeSaS', 'SekeSas', 'SokuSoS', 'SokusoS',
'SakosaS', 'sakosaS', 'SoSukiS', 'soSukiS', 'susekus', 'suSekus',
'sukeSos', 'SukeSos', 'sikosus', 'sikosuS', 'sikasus', 'sikaSus',
'SisikaS', 'Sisikas', 'susikas', 'Susikas', 'SaSakoS', 'SasakoS',
'SikuSis', 'sikuSis', 'sokasiS', 'sokasis', 'soSakas', 'sosakas',
'Sesakis', 'SesakiS', 'SikoSis', 'SikoSiS', 'SusekiS', 'SuSekiS',
'sokisoS', 'SokisoS', 'Sesikos', 'sesikos', 'sakuSes', 'sakuses',
'saSekeS', 'saSekes', 'saSikuS', 'SaSikuS', 'SekosaS', 'SekoSaS',
'Sosikos', 'SosikoS', 'Sosakis', 'sosakis', 'saSukes', 'sasukes',
'siSukiS', 'siSukis', 'siSokiS', 'SiSokiS', 'SesokaS', 'SeSokaS',
'sekasiS', 'SekasiS', 'sekisoS', 'sekisos', 'sokaSas', 'sokasas',
'SakeSes', 'sakeSes', 'SakiSus', 'SakiSuS', 'SukesiS', 'SukeSiS']