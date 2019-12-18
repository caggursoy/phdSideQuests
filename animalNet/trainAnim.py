# USAGE
# python trainAnim.py --dataset images --model cae-model.model
# import PlaidML first
# import plaidml.keras
# plaidml.keras.install_backend()
# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from keras.utils import to_categorical
from keras.utils import plot_model
from model.arch import modelArch
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default="images\\raw-img",
	help="path to input dataset")
ap.add_argument("-m", "--model", default="model0.model",
	help="path to output model")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
	help="path to output loss/accuracy plot")
args = vars(ap.parse_args())

# initialize the number of epochs to train for, initial learning rate,
# and batch size
EPOCHS = 100
INIT_LR = 1e-3  #1e-3
BS = 32
trgIm = [75,75,3]
noClass = 10

# initialize the data and labels
print("[INFO] loading images...")
data = []
labels = []

# grab the image paths and randomly shuffle them
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)

# def labeler
def switch_label(argument):
	switcher = {
		"butterfly" : 0,
		"cat" : 1,
		"chicken" : 2,
		"cow" : 3,
		"dog" : 4,
		"elephant" : 5,
		"horse" : 6,
		"sheep" : 7,
		"spider" : 8,
		"squirrel" : 9
	}
	return switcher.get(argument)

# loop over the input images
idx=0
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
	labels.append(switch_label(label))
	# print(label, switch_label(label))
	print('\t', round(100*idx/len(imagePaths),2) , '%...', end="\r")
	idx=idx+1
# scale the raw pixel intensities to the range [0, 1]

# data = np.array(data, dtype="float") / 255.0
data = np.array(data, dtype="float") / np.amax(data)
labels = np.array(labels)

# partition the data into training and testing splits using 60% of
# the data for training and the remaining 20% for testing and 20% for validation
(trainX, testX, trainY, testY) = train_test_split(data,
	labels, test_size=0.2, random_state=42)

# validation split
(trainX, valX, trainY, valY) = train_test_split(trainX,
	trainY, test_size=0.25, random_state=42)

# convert the labels from integers to vectors
trainY = to_categorical(trainY, num_classes=noClass) # convert string to int
testY = to_categorical(testY, num_classes=noClass)
valY = to_categorical(valY, num_classes=noClass)

print("Training size: ",str(int(100*trainX.size/data.size)),"%")
print("Test size: ",str(int(100*testX.size/data.size)),"%")
print("Validation size: ",str(int(100*valX.size/data.size)),"%")

# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

# initialize the model
print("[INFO] compiling model...")
model = modelArch.build(width=trgIm[0], height=trgIm[1], depth=trgIm[2], classes=noClass)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
# opt = SGD(lr=0.0001)
model.compile(loss="categorical_crossentropy", optimizer=opt,
	metrics=["accuracy"])

# train the network
print("[INFO] training network...")
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
	validation_data=(valX, valY), steps_per_epoch=len(trainX) // BS,
	epochs=EPOCHS, verbose=1, shuffle=True, max_queue_size=10)
# H = model.fit(x=trainX, y=trainY, validation_data=(valX, valY), steps_per_epoch=None,
# 	epochs=EPOCHS, verbose=1, shuffle=False)

# save the model to disk
print("[INFO] serializing network...")
model.save(args["model"])

# plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
N = EPOCHS
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])
