import numpy as np
from scipy.optimize import minimize

data = np.genfromtxt("SAheart.data.txt", delimiter=",", skip_header=1, dtype=None, encoding=None)

#Feature columns
feature_names = ['ldl', 'adiposity', 'typea', 'obesity', 'alcohol', 'age']
feature_indices = [2, 3, 6, 7, 8, 9]
label_index = 10  # chd

#Extract features and labels
X_all = np.array([[float(row[i]) for i in feature_indices] for row in data])
y_all = np.array([int(row[label_index]) for row in data])

#Labels are in -1, 1 for SVM
y_all = 2 * y_all - 1

#Last 16 examples
X = X_all[-16:]
y = y_all[-16:]

n_samples, n_features = X.shape
C = 2

#Linear kernel
K = X @ X.T
P = np.outer(y, y) * K

#Objective function
def objective(alpha):
    return 0.5 * alpha @ P @ alpha - np.sum(alpha)

#Gradient
def gradient(alpha):
    return P @ alpha - np.ones_like(alpha)

#Equality constraint
constraints = {'type': 'eq', 'fun': lambda a: np.dot(a, y), 'jac': lambda a: y}

#Bounds
bounds = [(0, C) for _ in range(n_samples)]

#Initial guess
alpha0 = np.zeros(n_samples)

# Solve
res = minimize(objective, alpha0, jac=gradient, constraints=constraints, bounds=bounds)
alpha_opt = res.x

print("\n===== PART A =====\n")

print("Dual variables (alpha):")
print(alpha_opt)

print("\n===== PART B =====\n")


w = np.sum((alpha_opt * y)[:, None] * X, axis=0)
print("Slope vector (w):")
print(w)

print("\n===== PART C =====\n")


support_indices = np.where((alpha_opt > 1e-5) & (alpha_opt < C - 1e-5))[0]
b_vals = y[support_indices] - X[support_indices] @ w
b = np.mean(b_vals)
print("Intercept (b):", b)

print("\n===== PART D =====\n")


#Decision function
decision_values = X @ w + b
predictions = np.sign(decision_values)

#Margin = 1
margins = y * decision_values

correct_outside = np.where((predictions == y) & (margins > 1))[0]
correct_on = np.where((predictions == y) & (np.isclose(margins, 1)))[0]
correct_inside = np.where((predictions == y) & (margins < 1))[0]
incorrect = np.where(predictions != y)[0]

print("Correctly classified outside margin:", correct_outside)
print("Correctly classified on margin:", correct_on)
print("Correctly classified inside margin:", correct_inside)
print("Incorrectly classified:", incorrect)

print("\n===== PART E =====\n")

print("Support vector indices:", np.where(alpha_opt > 1e-5)[0])

print("\n===== PART F =====\n")

distances = np.abs(decision_values) / np.linalg.norm(w)
margin = 1 / np.linalg.norm(w)
accuracy = np.mean(predictions == y)

print("Distances to hyperplane:", distances)
print("Margin size:", margin)
print("Accuracy:", accuracy)

print("\n===== PART G =====\n")

x_new = np.ones(X.shape[1])
pred_new = np.sign(x_new @ w + b)
print("Prediction for all features = 1:", int((pred_new + 1) // 2))  # Convert back to {0,1}