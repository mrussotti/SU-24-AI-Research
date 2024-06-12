import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

#generate synthetic data for clustering
X, _ = make_blobs(n_samples=100, centers=3, n_features=2, random_state=42)

#create + fit the model
model = KMeans(n_clusters=3, random_state=42)
model.fit(X)

#predict w/ the model
y_pred = model.predict(X)

#results
plt.scatter(X[:, 0], X[:, 1], c=y_pred, cmap='viridis', edgecolor='k', s=20)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('K-Means Clustering Demo')
plt.show()
