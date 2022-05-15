import numpy as np
import pickle
import random
corr = None
ifTest = False
Ztr = {}
Zte = {}

# States are tuples of the form (x,y) where both x,y belong to the closed interval [0,9].

# The terminology for action is :
# -1 for SELL
# 0 for HOLD
# 1 for BUY

# The returnNext function would take in the state and action, and return the next state, which you would get alongwith the price change associated with this tuple of (state,action)

# This might be different in different turns as this change is stochastic in general with only a co-relation to the (state, action) tuple.


def returnNext(state, action):
    # Returns (priceChange, nextState) as a tuple
    #nextState is actually a 2-tuple representing the state
    a,b = state
    L = []
    if ifTest:
        L = Zte[(a,b)]
    else:
        L = Ztr[(a,b)]
    r = L[random.randint(0,len(L)-1)]
    pricc = None
    if action==-1:
        if r[0]==0:
            pricc =  r[4]
        elif r[0]==1:
            pricc =  r[3]
        else:
            pricc =  -r[3]
    elif action==1:
        if r[2]==0:
            pricc =  r[4]
        elif r[2]==1:
            pricc =  r[3]
        else:
            pricc =  -r[3]
    else:
        if r[1]==0:
            pricc =  r[4]
        elif r[1]==1:
            pricc =  r[3]
        else:
            pricc =  -r[3]
    num = 3*(10*a + b) + action + 1

    F = corr[num,:]
    ch = np.random.choice(np.arange(0,100),p = list(F))
    ca = ch // 10
    cb = ch % 10
    return (pricc,(ca,cb))



# Train your Markov Decision Process, make use of the returnNext function to model and act on the priceChanges dependence on the states and actions
def Train():
    results = [[0]*10]*10
    for j in range(0,10):
    	for k in range(0,10):
            state = (j,k)
            (pricc1, temp1) = returnNext(state, -1)
            (pricc2, temp2) = returnNext(state, 0)
            (pricc3, temp3) = returnNext(state, 1)
            maxc = max(pricc1, pricc2, pricc3)

            if maxc==pricc1:
	            results[j][k] = -1
            elif maxc==pricc3:
	            results[j][k] = 1
            else:
	            results[j][k] = 0

    return results
    

# This you need to write after training your MDP, this should just take in the state and return the Action you would perform
# Please do not make use of the returnNext function inside here, that would defeat the purpose of training the model, as it would be known to you!

def Run(state, results):
    (j,k) = state
    act = results[j][k]
    return act
    

# This is the main function, you don't need to tamper with it!
def mainRun(iter = 1000):
    initstate = (random.randint(0,9),random.randint(0,9))
    i = 0
    initprice = 100.00
    price = initprice
    balance = 0
    bondbal = 0
    networth = 0
    st = initstate
    while i < iter:
        act = Run(st, results)
        pricCh, ns = returnNext(st,act)
        price += pricCh
        if act==1:
            balance -= 10*price
            bondbal += 10
        elif act==-1:
            balance += 10*price
            bondbal -= 10
        
        networth = balance + bondbal*price
        st = ns
        print('Your Networth has went from 0 to ',networth)
        i+=1














ftr = input('Test : Filename to read from?')
fte = input('Train : Filename to read?')


with open(ftr,'rb') as f:
    Ztr = pickle.load(f)

with open(fte,'rb') as f:
    Zte = pickle.load(f)

with open('correlations.npy','rb') as f:
    corr = np.load(f)

ifTest  = False
results = Train()
ifTest = True
mainRun()
