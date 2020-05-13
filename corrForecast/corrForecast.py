import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
#

sales_data = pd.read_csv('EUR_TRY Historical Data.csv',header=0)
# print('Keys',sales_data.keys())
# print('Data\n',sales_data)
# print(sales_data['Date'])
# sales_data.plot()
sales_data2 = sales_data.iloc[::-1]
currData = sales_data2['Price'].reset_index(drop=True)
# print(currData)

def autoCorr(data,a=0,b1=0,b2=0,b3=0):
    next = np.zeros(len(data))
    for i in range(3,len(data)):
        next[i-3] = a + b1*data[i-1] + b2*data[i-2] + b3*data[i-3]
    i = len(data)
    next[len(data)-3] = a + b1*data[i-1] + b2*data[i-2] + b3*data[i-3]
    next[len(data)-2] = a + b2*data[i-2] + b3*data[i-3]
    next[len(data)-1] = a + b3*data[i-3]
    return next

a=0;b1=0.5;b2=0.3;b3=0.1
finArr = autoCorr(currData,a,b1,b2,b3)
finArr = pd.DataFrame(data=finArr)[0]

#
# normaliser(currData,finArr,a,b1,b2,b3)
def gradDesc(X,Y):
    m = 0
    c = 0

    L = 0.0001  # The learning Rate
    epochs = 1000  # The number of iterations to perform gradient descent

    n = float(len(X)) # Number of elements in X

    # Performing Gradient Descent
    for i in range(epochs):
        Y_pred = m*X + c  # The current predicted value of Y
        D_m = (-2/n) * sum(X * (Y - Y_pred))  # Derivative wrt m
        D_c = (-2/n) * sum(Y - Y_pred)  # Derivative wrt c
        m = m - L * D_m  # Update m
        c = c - L * D_c  # Update c

    # print (m, c)

    # Making predictions
    Y_pred = m*X + c

    # plt.scatter(X, Y)
    # plt.plot([min(X), max(X)], [min(Y_pred), max(Y_pred)], color='red')  # regression line
    # plt.show()
    return X,Y_pred
regX, regY = gradDesc(currData,finArr)
# print(regX,'\n',regY)

# for i in range(len(finArr)):
#     print(finArr[i],currData[i])
plt.plot(sales_data['Date'],regX,label='Actual')
plt.plot(sales_data['Date'],regY,label='Predicted')
plt.legend()
plt.xticks(rotation=90)
# plt.autoscale(enable=True)
plt.savefig('output2.png',dpi=1000)
