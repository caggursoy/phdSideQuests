from psychopy import visual, core, event, monitors
import os
import platform

### Define functions ###
# function that creates visual stimuli
def visStim():
    #create a window
    mywin = visual.Window([800,600],monitor="testMonitor", units="deg")

    img = visual.ImageStim(win=mywin, image="cagatay-louvre.jpg", units="pix")

    img.size = [img.size[0]*.45, img.size[1]*.45]
    img.draw()

    mywin.flip()
    core.wait(3)

    # for mon in monitors.getAllMonitors():
    #     print(mon, monitors.Monitor(mon).getSizePix())

    mywin.close()
    core.quit()
# function to clear the screen
def clear():
    plat = platform.system()
    if plat == 'Linux' or plat == 'Darwin':
        os.system('clear')
    else:
        os.system('cls')
    return plat
