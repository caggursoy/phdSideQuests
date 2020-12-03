# import packages
import functions
import numpy as np
import random
import matplotlib.pyplot as plt
# define variables
t_blockAdm = np.arange(0,40,step=2)
t_blockRest = np.arange(40,60,step=2)
# seed = random.randint(0,100)

# define main
def main():
    print("Running main...")
    usPro = input(prompt='(S)ingle or (M)ulti run?..')
    if usPro.lower()=='m':
        rng = 10 # number of runs desired
        resList = [] # init empty list
        for p in range(rng):
            seed = random.randint(0,100)
            activTup = functions.randAdmin(t_blockAdm, t_blockRest, seed, pltFlag=False)
            unzipTup = list(zip(*activTup))
            resList.extend(unzipTup[1])
        functions.plotMult(resList, len(resList), rng)
    elif usPro.lower()=='s':
        seed = random.randint(0,100)
        activTup = functions.randAdmin(t_blockAdm, t_blockRest, seed)
    else:
        print('Wrong input! Terminating program...')

# run main
if __name__ == "__main__":
    main()
