import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
#

def autoCorr(data,a=0,b1=0,b2=0,b3=0):
    next = np.zeros(len(data))
    for i in range(3,len(data)):
        next[i-3] = a + b1*data[i-1] + b2*data[i-2] + b3*data[i-3]
    i = len(data)
    next[len(data)-3] = a + b1*data[i-1] + b2*data[i-2] + b3*data[i-3]
    next[len(data)-2] = a + b2*data[i-2] + b3*data[i-3]
    next[len(data)-1] = a + b3*data[i-3]
    return next

def gradDesc2(X,Y,L=0.0001,epochs=1000):
    m1 = 0; m2 = 0; m3 = 0; c = 0;
    n = float(len(X)) # Number of elements in X
    for i in range(epochs):
        Y_pred = m1*np.roll(X,1) + m2*np.roll(X,2) + m3*np.roll(X,3) + c
        D_m1 = (-2/n) * sum(np.roll(X,1) * (Y - Y_pred))  # Derivative wrt m
        D_m2 = (-2/n) * sum(np.roll(X,2) * (Y - Y_pred))  # Derivative wrt m
        D_m3 = (-2/n) * sum(np.roll(X,3) * (Y - Y_pred))  # Derivative wrt m
        D_c = (-2/n) * sum(Y - Y_pred)  # Derivative wrt c
        m1 = m1 - L * D_m1  # Update m
        m2 = m2 - L * D_m2  # Update m
        m3 = m3 - L * D_m3  # Update m
        c = c - L * D_c  # Update c
    Y_pred = m1*np.roll(X,1) + m2*np.roll(X,2) + m3*np.roll(X,3) + c
    err = abs(Y_pred - X)
    return X, Y_pred, err, [m1,m2,m3,c]

def predFut(data,varList,daysFut):
    outList = []
    dataList = list(data)
    print(dataList)
    for i in range(0,daysFut):
        predY = varList[0]*np.roll(dataList,(2*i+1))[-1] + varList[1]*np.roll(dataList,(2*i+2))[-1] + varList[2]*np.roll(dataList,(2*i+3))[-1] + varList[3]
        print(predY)
        outList.append(predY)
        dataList.append(predY)
    # Y_pred = varList[0]*np.roll(data,1) + varList[1]*np.roll(data,2) + varList[2]*np.roll(data,3) + varList[3]
    return outList

def gradDesc(X,Y,L=0.0001,epochs=1000):
    m = 0; c = 0;
    n = float(len(X)) # Number of elements in X

    # Performing Gradient Descent
    for i in range(epochs):
        Y_pred = m*X + c  # The current predicted value of Y
        D_m = (-2/n) * sum(X * (Y - Y_pred))  # Derivative wrt m
        D_c = (-2/n) * sum(Y - Y_pred)  # Derivative wrt c
        m = m - L * D_m  # Update m
        c = c - L * D_c  # Update c
    # Making predictions
    Y_pred = m*X + c
    print(m,c)
    err = abs(Y_pred - X)
    return X, Y_pred, err

def months(argument):
    switcher = {
        "Jan":'1',
        "Feb":'2',
        "Mar":'3',
        "Apr":'4',
        "May":'5',
        "Jun":'6',
        "Jul":'7',
        "Aug":'8',
        "Sep":'9',
        "Oct":'10',
        "Nov":'11',
        "Dec":'12'
    }
    return switcher.get(argument, "Invalid month")

def dateConv(data):
    dates = []
    for d in data:
        x = d.split(',')
        xx = x[0].split(' ')
        xx.append(x[1])
        xx[0] = months(xx[0])
        outStr = xx[1]+' '+xx[0]+xx[2]
        dates.append(outStr)
    return(dates)

def plotter(dataX,dataY,showSave=True,name='outImg.png',dpi=500):
    plt.plot(dataX,dataY,label='Actual')
    plt.plot(dataX,regY,label='Predicted')
    plt.legend()
    plt.xticks(rotation=90)
    plt.autoscale(enable=True)
    if showSave:
        plt.show()
    else:
        plt.savefig(name,dpi=dpi)
