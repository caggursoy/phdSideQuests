import os
import platform
import functions

# define main
def main():
    functions.clear()
    functions.visStim()

# run main
if __name__ == '__main__':
    print('Running main...')
    main()

# def main():
#     plat = functions.clear() # get the name of the platform
#     menu = input('Please enter menu option: \n0 - Folder Select\n1 - Image Info\n2 - Resize Images\n')
#     if int(menu) == 0:
#         initPath = input('Please enter initial path\n')
#         folder0 = functions.folderSelector(initPath, plat)
#         print ('Selected folder is: \n' + folder0)
#     elif int(menu) == 2:
#         initPath = input('Please enter initial path\n')
#         imgFolder = functions.folderSelector(initPath, plat)
#         # imgFolder = 'C:\Local\LocalRepos\onlineTask\pseuRand2\Images' #debug
#         print('Selected folder is: \n' + imgFolder)
#         functions.imgInf(imgFolder)
#     else:
#         print('End')
