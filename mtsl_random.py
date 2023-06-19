from Lambert import *
from random import randint, sample
from itertools import permutations
from sys import argv

sigma = {'0','1','2','3','4','5'}



def generate_mtsl_acceptor():
    '''
    Using the alphabet sigma from above, and the mtsl_acceptor() function from Lambert.py, this generates a random MTSL-2 grammar
    '''
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

'''
Use command-line parameters to run this. 
The first parameter is the length of the longest sample in the "training data", while the second parameter is the length of the longest sample in the "test data"

If I remember correctly, I ended up training on all accepted strings up to length 7, and at that point it had a characteristic sample to give the right judgement
    for all strings (though I only exhaustively tested for strings of up to length 9)
That was for MTSL2, for other classes, this length would change
'''
sigstrain = list(star(sigma, int(argv[1])))
sigstest = list(star(sigma, int(argv[2])))
verbose = False if (len(argv) >=4 and argv[3] == 'quick') else True

counterexample = False
i = 0
while not counterexample:
    i += 1
    print(f'\nattempt #{i}', end='')
    acceptor = generate_mtsl_acceptor()
    g = learn(filter(acceptor, sigstrain), k=2,m=1) #only learn on the strings from sigstrain which are accepted by the random mtsl grammar
    if bad := wrong(g, acceptor, sigstest, verbose=verbose): #if there are any strings for which the learned grammar disagrees with the target grammar, we have a counterexample to show that the learner has not learned the grammar
        print(f"\rfound counterexample on attempt #{i}:")
        print("acceptor:", acceptor(None))
        print("grammar:", g)
        print("misses:", bad)
        counterexample = True
    else:
        print("grammar learned successfully")
