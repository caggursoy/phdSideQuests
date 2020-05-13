from funcs import gradDesc2
from funcs import dateConv

# Import data into pandas and fix
sales_data = pd.read_csv('EUR_TRY Historical Data.csv',header=0)
sales_data2 = sales_data.iloc[::-1]
targetData = sales_data2['Price'].reset_index(drop=True)
outDates = dateConv(sales_data2['Date'])

L=0.0001; epochs=1000
varList = [0,0,0,0]
regX, regY, err, varList = gradDesc2(targetData, targetData, L=L, epochs=epochs)
# print(m,c)
print(varList)

predY = predFut(targetData,varList,1000)
print(predY)
plt.plot(predY)
plt.show()

plt.plot(outDates,regX,label='Actual')
plt.plot(outDates,regY,label='Predicted')
plt.legend()
# plt.xticks(rotation=90)
plt.autoscale(enable=True)
plt.show()
# plt.savefig('output2.png',dpi=1000)
