# import packages
import random
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

# randomly assign alcohol or control administration. alcohol = 2 & control = 1
def randAdmin(timeAdm, timeRest, seed, pltFlag = True):
    random.seed(seed)
    n = int(len(timeAdm))
    nRest = int(len(timeRest))
    time = list(timeAdm)+list(timeRest)
    activList = [1]*int(n/4) + [2]*int(n/4)
    random.shuffle(activList)
    insIdx = np.arange(1,60,step=2)
    for idx in insIdx:
        activList.insert(idx, 0)
    resList = [0] * nRest
    activList = activList+resList
    activTup = tuple(zip(time,activList))
    if pltFlag:
        print('Plotting random run:')
        unzipTup = list(zip(*activTup))
        plt.plot(unzipTup[0], unzipTup[1], drawstyle='steps-post')
        plt.ylim(0,2.2)
        plt.yticks(np.arange(0, 3, step=1), ('Clean','Control','Alcohol'))
        plt.xticks(np.arange(0, 60, step=4))
        plt.grid()
        plt.show()

    return activTup

def plotMult(resList, leng, rng):
    step = int(2*leng/rng)
    xtcks = list(map(str, np.arange(0,leng*2,step=step)))
    plt.plot(resList, drawstyle='steps-post')
    plt.ylim(0,2.2)
    plt.yticks(np.arange(0, 3, step=1), ('Clean','Control','Alcohol'))
    plt.xticks(np.arange(0, leng, step=step/2), xtcks)
    plt.grid()
    plt.show()
