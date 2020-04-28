import os
import sys
from pyboy import PyBoy, WindowEvent # isort:skip

def loadCartridge(filePath, quiet=True, emSpd=1):
    pyboy = PyBoy(filePath, window_type="headless" if quiet else "SDL2",
    window_scale=3, debug=not quiet, game_wrapper=True)
    pyboy.set_emulation_speed(emSpd)
    pyboy.cartridge_title() == "SUPER MARIOLAN"
    return pyboy

def startMario(pyboy):
    mario = pyboy.game_wrapper()
    mario.start_game()
    mario.score == 0
    mario.lives_left == 2
    mario.time_left == 400
    mario.world == (1, 1)
    mario.fitness == 0
    return(mario)

def moveRight(pyboy, mario):
    pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
    print('moveRight\n',mario)

def playLoop(pyboy,mario,flag=True):
    # moveRight(pyboy, mario)
    while flag:
        moveRight(pyboy, mario)
        pyboy.tick()
