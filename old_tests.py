from Lambert import *


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