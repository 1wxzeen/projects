import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("LAozone.data", delimiter = ",", skiprows = 1) #We set skiprows = 1 becuase we want to skip the first row; this is the only instance of non-pythnonicism
#now we have just the data of numbers, which should be (310, 10)

Y = data[:, 0] #from __data__, you take all the rows (310) and from one column (0)

#the features of interest are columns 2, 3, 4, and 8 from the 0 to N pythonic scale
X = data[:, [2, 3, 4, 8]]
# now `we have a 310 by 4 matrix
#however, we need to account for the intercept as the following:
#w = the column vector <w0, w1, w2, w3, w4> and there are 5 rows
# Since prediction = Y - Xw, X needs to have 5 columns for the multiplication
# since the first column must be a column of w0 anyways, we need to add in a column of 1s to X
X = np.column_stack((np.ones(X.shape[0]), X))

#Linear algebra block
#w = (XTX)-1(XTY)

XT_X = X.T @ X
XT_Y = X.T @ Y
XT_X_inv = np.linalg.inv(XT_X)
w = XT_X_inv @ XT_Y
#print(w) #this gives us the least squares estimate of the parameter vector; its a 5x1 column vector

w0 = w[0]
w1 = w[1]
w2 = w[2]
w3 = w[3]
w4 = w[4]

print(w)

print(f"The estimated slope of wind is {w1}")    
print(f"The estimated intercept is {w0}")


# The residual vector is defined as ri = Yi - Yifitted for the values i till N
#Y fitted equals Xw; we already have Y regular

Xw = X @ w
residual = Y - Xw

plt.scatter(Xw, residual, color = "orange", alpha = .7)
plt.axhline(y = 0, color = "red", linestyle = "--")
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.title("Residual plot")
plt.show()

#now to predict ozone for w1 = 5, w2 = 60, w3 = 50, w4 = 200
# Prediction = w0 + w1X1 + w2X2 +...+ w5X5

new_features = np.array([1, 5, 60, 50, 200])

prediction = new_features @ w

print(new_features.shape)

print(prediction)



