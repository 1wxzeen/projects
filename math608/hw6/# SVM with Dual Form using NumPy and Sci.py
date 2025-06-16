# SVM with Dual Form using NumPy and SciPy only
import numpy as np
from scipy.optimize import minimize

# Load the data manually without pandas
X = np.loadtxt("nci.data (1).csv", delimiter=",").T  # Transpose so samples are rows
with open("nci.label.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Filter NSCLC and RENAL only
labels = np.array(labels)
mask = (labels == "NSCLC") | (labels == "RENAL")
X = X[mask]
y = np.where(labels[mask] == "NSCLC", 1, -1)

# Compute the Kernel matrix (linear kernel)
K = X @ X.T
P = np.outer(y, y) * K
n = X.shape[0]

# Dual objective function
def objective(alpha):
    return 0.5 * alpha @ P @ alpha - np.sum(alpha)

def zerofun(alpha):
    return np.dot(alpha, y)

# Bounds and constraints
bounds = [(0, None) for _ in range(n)]
constraints = {"type": "eq", "fun": zerofun}
alpha0 = np.zeros(n)

# Solve the optimization problem
res = minimize(objective, alpha0, bounds=bounds, constraints=constraints)
alphas = res.x

# Compute the weight vector w
w = ((alphas * y)[:, None] * X).sum(axis=0)

# Compute the bias term b
support_indices = np.where(alphas > 1e-5)[0]
b = np.mean([y[i] - np.dot(w, X[i]) for i in support_indices])

# Print support vector indices
print("Support vector indices:", support_indices)

# Compute distances to hyperplane
distances = (X @ w + b) / np.linalg.norm(w)

# Compute accuracy
predictions = np.sign(X @ w + b)
accuracy = np.mean(predictions == y)
print("Accuracy:", accuracy)

# Compute margin
margin = 1 / np.linalg.norm(w)
print("Margin:", margin)

# Predict for x = all ones
x_new = np.ones(X.shape[1])
pred_label = np.sign(np.dot(w, x_new) + b)
print("Prediction for all features = 1:", "NSCLC" if pred_label == 1 else "RENAL")
