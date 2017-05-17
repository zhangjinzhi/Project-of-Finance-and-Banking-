from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
# preprocessing function
from sklearn.preprocessing import StandardScaler
from numpy import *

house_dataset = datasets.load_boston()
house_data = house_dataset.data
print house_data
house_price = house_dataset.target
print house_price
x_train, x_test, y_train, y_test = train_test_split(house_data, house_price, test_size = 0.2)
# f(x) = (x - means) / standard deviation
scaler = StandardScaler()
scaler.fit(x_train)
# standardization
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# construct SVR model
svr = SVR(kernel = 'rbf')
svr.fit(x_train, y_train)
y_predict = svr.predict(x_test)
result = hstack((y_test.reshape(-1, 1), y_predict.reshape(-1, 1)))
print(result)