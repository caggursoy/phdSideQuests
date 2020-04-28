import functions

pyboy = functions.loadCartridge('/home/cagatay/Documents/repos/phdSideQuests/pyBoyTrials/ROMs/supermario.gb', emSpd = 1)
mario = functions.startMario(pyboy)
functions.playLoop(pyboy, mario)
