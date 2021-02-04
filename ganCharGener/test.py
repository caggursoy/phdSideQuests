### using https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-from-scratch-for-mnist-handwritten-digit-classification/ as guide
import plaidml.keras
plaidml.keras.install_backend()
import scipy.io as sio
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# baseline cnn model for mnist
from numpy import mean
from numpy import std
from matplotlib import pyplot
from sklearn.model_selection import KFold
# from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.models import load_model
from keras.utils import plot_model

model = load_model('model.model')
plot_model(model, to_file= str('model.png'))
