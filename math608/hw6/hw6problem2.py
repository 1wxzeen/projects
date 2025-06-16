import numpy as np
from scipy.optimize import minimize
from sklearn.svm import SVC

# ----------------------------------------------------------------------
# (A) SciPy-based Hard-Margin SVM
# ----------------------------------------------------------------------
print("========== PROBLEM 2 (Part 2) - SciPy Version ==========\n")

# 1) Load the data
X = np.genfromtxt("nci.data.csv", delimiter=",", dtype=float).T
X = np.nan_to_num(X, nan=0.0)  # fill any NaNs if present

with open("nci.label.txt", "r") as f:
    labels = [line.strip() for line in f if line.strip() != ""]

# If there's a mismatch in lengths, patch with a dummy label
if len(labels) < X.shape[0]:
    labels.append("UNKNOWN")

labels = np.array(labels)

# Filter for NSCLC (+1) vs RENAL (-1)
mask = (labels == "NSCLC") | (labels == "RENAL")
X = X[mask]
y = np.where(labels[mask] == "NSCLC", 1, -1)

# 2) Construct the SVM Dual
K = X @ X.T
P = np.outer(y, y) * K
n = X.shape[0]

def svm_dual_objective(alpha):
    return 0.5 * alpha @ P @ alpha - np.sum(alpha)

def svm_dual_constraint(alpha):
    return np.dot(alpha, y)

bounds = [(0, None)] * n
constraints = {"type": "eq", "fun": svm_dual_constraint}
alpha0 = np.zeros(n)

# 3) Solve the constrained QP with SciPy
res = minimize(svm_dual_objective, alpha0, bounds=bounds, constraints=constraints)
alphas = res.x

# (a) Dual variables
print("(a) Dual variables (alphas):\n", alphas, "\n")

# (b) Slope vector w
w = ((alphas * y)[:, None] * X).sum(axis=0)
print("(b) Slope vector (w):\n", w, "\n")

# (c) Intercept b
sv_indices = np.where(alphas > 1e-5)[0]
b = np.mean([y[i] - np.dot(w, X[i]) for i in sv_indices])
print("(c) Intercept (b):\n", b, "\n")

# (d) Support vector indices
print("(d) Support vector indices:\n", sv_indices, "\n")

# (e) Distances & Accuracy
distances = (X @ w + b) / np.linalg.norm(w)
predictions = np.sign(X @ w + b)
accuracy = np.mean(predictions == y)
print("(e) Distances from hyperplane:\n", distances, "\n")
print("    Accuracy:", accuracy, "\n")

# (f) Margin
margin = 1.0 / np.linalg.norm(w)
print("(f) Margin:", margin, "\n")

# (g) Predict for x=all ones
x_new = np.ones(X.shape[1])
pred_value = np.dot(w, x_new) + b
pred_label = 1 if pred_value >= 0 else -1
print("(g) Prediction for x=all ones:", "NSCLC" if pred_label == 1 else "RENAL")

# ----------------------------------------------------------------------
# (B) Scikit-learn-based Hard-Margin SVM
# ----------------------------------------------------------------------
print("\n========== PROBLEM 2 (Part 2) - Scikit-Learn Version ==========\n")

clf = SVC(kernel="linear", C=1e10)  # large C => approximate hard margin
clf.fit(X, y)

# (a) Dual variables:
# scikit-learn only stores alpha_i*y_i for support vectors in clf.dual_coef_[0].
# We can reconstruct the full alpha array, with zeros for non-SVs:
n = len(y)
alphas_skl = np.zeros(n, dtype=float)
alpha_y = clf.dual_coef_[0]        # shape: (1, n_SV), alpha_i * y_i
support_vecs = clf.support_        # indices of support vectors
for i, sv_ix in enumerate(support_vecs):
    alphas_skl[sv_ix] = alpha_y[i] / y[sv_ix]

print("(a) Dual variables (alphas) from scikit-learn:\n", alphas_skl, "\n")

# (b) w
w_skl = clf.coef_.ravel()
print("(b) Slope vector (w):\n", w_skl, "\n")

# (c) b
b_skl = clf.intercept_[0]
print("(c) Intercept (b):\n", b_skl, "\n")

# (d) Support vector indices
print("(d) Support vector indices:\n", support_vecs, "\n")

# (e) Distances & Accuracy
distances_skl = (X @ w_skl + b_skl) / np.linalg.norm(w_skl)
predictions_skl = clf.predict(X)
accuracy_skl = np.mean(predictions_skl == y)
print("(e) Distances from hyperplane:\n", distances_skl, "\n")
print("    Accuracy:", accuracy_skl, "\n")

# (f) Margin
margin_skl = 1.0 / np.linalg.norm(w_skl)
print("(f) Margin:", margin_skl, "\n")

# (g) Predict for x=all ones
pred_value_skl = np.dot(w_skl, x_new) + b_skl
pred_label_skl = 1 if pred_value_skl >= 0 else -1
print("(g) Prediction for x=all ones:", "NSCLC" if pred_label_skl == 1 else "RENAL")
