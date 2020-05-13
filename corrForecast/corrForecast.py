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
def gradDesc(X,Y,L=0.0001,epochs=1000):
    m = 0; c = 0; err = abs(Y - X)
    # L = 0.0001  # The learning Rate
    # epochs = 1000  # The number of iterations to perform gradient descent

    n = float(len(X)) # Number of elements in X

    # Performing Gradient Descent
    for i in range(epochs):
        Y_pred = m*X + c  # The current predicted value of Y
        D_m = (-2/n) * sum(X * (Y - Y_pred))  # Derivative wrt m
        D_c = (-2/n) * sum(Y - Y_pred)  # Derivative wrt c
        print(D_m,np.isnan(D_m))
        if np.isnan(D_m) or np.isnan(D_c):
            m = m; c = c
        else:
            m = m - L * D_m  # Update m
            c = c - L * D_c  # Update c
    # Making predictions
    # print('m:',m,'c:',c)
    Y_pred = m*X + c
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
outDates = dateConv(sales_data2['Date'])


L=0.000001; epochs=1000
regX, regY, err = gradDesc(currData,finArr,L=0.000001,epochs=1000)
# print(np.isnan(err))
while max(err) > 0.2 and L<1:
    L = L*10; epochs = epochs*2
    regX, regY, err = gradDesc(currData, finArr, L=L, epochs=epochs)
    # print(max(err))

print(regX)
print(regY)

for p in range(regXVal):
    print(regXVal[p],regYVal[p])

plt.plot(outDates,regX,label='Actual')
plt.plot(outDates,regY,label='Predicted')
plt.legend()
plt.xticks(rotation=90)
# plt.show()
plt.autoscale(enable=True)
plt.savefig('output2.png',dpi=1000)
