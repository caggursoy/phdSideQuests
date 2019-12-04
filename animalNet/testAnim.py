# USAGE
# python test_network.py --model cae-model.model
# import PlaidML first
import plaidml.keras
plaidml.keras.install_backend()
# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras.utils import plot_model
from keras import backend as K
from keras.models import Model
import tensorflow as tf
import numpy as np
import argparse
import imutils
import cv2
import os, random
from shutil import copyfile
import matplotlib.pyplot as plt
import pandas as pd
# import randomTargets

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,)
help="path to trained model model"
args = vars(ap.parse_args())

listIm = os.listdir("animals10/tests")
if '.DS_Store' in listIm:
  listIm.remove('.DS_Store')# if .DS_Store exists

# define variables
faceAges = []
predictedList = []
score = 0;
range10 = 0;
range5 = 0;
outOf = 0;
idx = 0;
idx2 = 0;
layerNames = []
auxLayerNames = []
actvList = []
sumList = []
##
conv2d_1List = []
activation_1List = []
max_pooling2d_1List = []
conv2d_2List = []
activation_2List = []
max_pooling2d_2List = []
##
imNameList = []
activationsList = []
layerNamesList = []
resList = []

# empty the image save folder
# auxPath = "/resultImages"
# filelist = [ f for f in os.listdir(auxPath)]
# for f in filelist:
#   os.remove(os.path.join(auxPath, f))
# begin the actual process
for imName in listIm:
  idx2 = 0;
  print(round((100*listIm.index(imName))/len(listIm),2),"%...",end="\r")
  auxName = imName
  imName = "animals10/tests/"+imName
  # print(imName)
  # load the image
  image = cv2.imread(imName)
  orig = image.copy()

  # pre-process the image for classification
  image = cv2.resize(image, (30, 30)) # 30,30
  image = image.astype("float") / 255.0
  image = img_to_array(image)
  image = np.expand_dims(image, axis=0)

  # load the trained convolutional neural network
  model = load_model(args["model"])
  # Save model img to file
  plot_model(model, show_shapes=True, to_file= str(args["model"])[0:-6]+'.png')

  # classify the input image
  results = model.predict(image)[0]
  resList.append(results)
  label = np.argmax(results)
  predictedList.append(label)
  imNameList.append(imName)

  # for layer in model.layers[:11]:
  #   layer_outputs = layer.output
  #   if idx < 11:
  #     layerNames.append(layer.name)
  #     idx += 1
  # for layer in model.layers[:11]: # to run make in [:11]
  #   layer_outputs = layer.output
  #   activation_model = Model(inputs=model.input, outputs=layer_outputs)
  #   # Creates a model that will return these outputs, given the model input
  #   activations = activation_model.predict(image)
  #   direc = 'intmLayerPlotsHappy/'+layerNames[idx2]
  #   layer_activation = activations[0]
  #   if len(layer_activation.shape) == 3:
  #     if not os.path.exists(direc):
  #       os.makedirs(direc)
  #     plt.matshow(layer_activation[:, :, 4])
  #     plt.colorbar()
  #     plt.savefig(direc+'/'+auxName+'_Intm.png')
  #     plt.close()
  #   else:
  #     imNameList.append(imName)
  #     layerNamesList.append(layerNames[idx2])
  #     activationsList.append(layer_activation)
  #     direc = 'intmLayerHeatmapsHappy/'+layerNames[idx2]
  #     if not os.path.exists(direc):
  #       os.makedirs(direc)
  #     x = np.linspace(1,len(layer_activation),len(layer_activation))
  #     xloc = np.linspace(0,len(layer_activation),50)
  #     y = layer_activation[:]
  #
  #     # fig, (ax,ax2) = plt.subplots(nrows=2, sharex=True)
  #     extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
  #     im1 = plt.imshow(y[np.newaxis,:], cmap="plasma", aspect="auto", extent=extent)
  #     # ax.set_xticks(xloc)
  #     # ax.set_yticks([])
  #     # ax.set_xlim(extent[0], extent[1])
  #     # ax2.plot(x,y)
  #     # fig.colorbar(im1, ax=ax, orientation='vertical')
  #     plt.colorbar(im1, orientation='horizontal')
  #     plt.tight_layout()
  #     plt.savefig(direc+'/'+auxName+'_Map.png')
  #     plt.close()

  idx2+=1

def switch_label(argument):
	switcher = {
		0 : "butterfly" ,
		1 : "cat" ,
		2 : "chicken",
		3 : "cow",
		4 : "dog",
		5 : "elephant",
		6 : "horse",
		7 : "sheep",
		8 : "spider",
		9 : "squirrel"
	}
	return switcher.get(argument)

for p in range(len(predictedList)):
    # print("Actual: ", imNameList[p], "\t","Final Prediction: ", switch_label(predictedList[p]), "\n", "Probs: ", resList[p])
    print("Actual: ", imNameList[p], "\tFinal Prediction: ", switch_label(predictedList[p]))
