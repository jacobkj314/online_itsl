from Lambert import *
from random import randint, sample
from itertools import permutations
from sys import argv

sigma = {'0','1','2','3','4','5'}



def generate_mtsl_acceptor():
    tsl_grammars = list()
    for _ in range(randint(2,5)):#pick 2-5 tiers
        tier = sample(list(sigma), randint(3,5)) #pick 3-5 symbols for the tier
        if randint(1, 100) < 5:#possbly add word boundaries to the tier
            tier.append('<')
        if randint(1, 100) < 5:
            tier.append('<')
        poss = list(permutations(tier, 2))
        restrictions = sample(poss, randint(3,5))#sample 3-5 possible restrictions for the tier
        tsl_grammars.append((tier, restrictions))
    return mtsl_acceptor(tsl_grammars)
    #return lambda w : all(acceptor(w) for acceptor in acceptors) if w is not None else [acceptor(None) for acceptor in acceptors]


sigstrain = list(star(sigma, int(argv[1])))
sigstest = list(star(sigma, int(argv[2])))

counterexample = False
i = 0
while not counterexample:
    i += 1
    print(f'\nattempt #{i}', end='')
    acceptor = generate_mtsl_acceptor()
    g = learn(filter(acceptor, sigstrain), k=2,m=1)
    if bad := wrong(g, acceptor, sigstest):
        print(f"\rfound counterexample on attempt #{i}:")
        print("acceptor:", acceptor(None))
        print("grammar:", g)
        print("misses:", bad)
        counterexample = True
