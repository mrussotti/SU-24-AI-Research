import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression

#data setup
X, y = make_regression(n_samples=100, n_features=1, noise=10, random_state=42)

#create + fit the model
model = LinearRegression()
model.fit(X, y)

#predict w/ the model
y_pred = model.predict(X)

#results
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X, y_pred, color='red', linewidth=2, label='Linear Regression')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression Demo')
plt.legend()
plt.show()
