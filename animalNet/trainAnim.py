# USAGE
# python trainAnim.py --dataset images --model cae-model.model
# import PlaidML first
import plaidml.keras
plaidml.keras.install_backend()
# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from keras.utils import to_categorical
from keras.utils import plot_model
# from pyimagesearch.lenet import LeNet
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
ap.add_argument("-m", "--model", default="model0.model",
	help="path to output model")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
	help="path to output loss/accuracy plot")
args = vars(ap.parse_args())

# initialize the number of epochs to train for, initial learning rate,
# and batch size
EPOCHS = 500
INIT_LR = 1e-3  #1e-3
BS = 32
trgIm = [240,240,3]

# initialize the data and labels
print("[INFO] loading images...")
data = []
labels = []

# grab the image paths and randomly shuffle them
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)

# loop over the input images
for imagePath in imagePaths:
	# load the image, pre-process it, and store it in the data list
	image = cv2.imread(imagePath)
	dims = image.shape
	if dims[0] != trgIm[0] or dims[1] != trgIm[1]:
		image = cv2.resize(image, (trgIm[0], trgIm[1]))
	image = img_to_array(image)
	data.append(image)
	# extract the class label from the image path and update the
	# labels list
	label = imagePath.split(os.path.sep)[-2]
	labels.append(label)

# scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

print(data.shape)
print(labels.shape)

# partition the data into training and testing splits using 60% of
# the data for training and the remaining 20% for testing and 20% for validation
(trainX, testX, trainY, testY) = train_test_split(data,
	labels, test_size=0.2, random_state=42)

# validation split
(trainX, valX, trainY, valY) = train_test_split(trainX,
	trainY, test_size=0.25, random_state=42)

# convert the labels from integers to vectors
trainY = to_categorical(trainY, num_classes=94)
testY = to_categorical(testY, num_classes=94)
valY = to_categorical(valY, num_classes=94)

print("Training size: ",str(int(100*trainX.size/data.size)),"%")
print("Test size: ",str(int(100*testX.size/data.size)),"%")
print("Validation size: ",str(int(100*valX.size/data.size)),"%")
