import numpy as np
from scipy.optimize import minimize
from sklearn.svm import SVC

# ========================================================
#   PROBLEM 3 - Hard-Margin SVM with SciPy & Scikit-learn
# ========================================================

# --------------------------------------------------------
#              SciPy Version
# --------------------------------------------------------
print("===== Output from SciPy (Problem 3) =====\n")

# 1) Load and parse SAheart.data
data = np.genfromtxt("SAheart.data", delimiter=",", skip_header=1, dtype=None, encoding=None)

with open("SAheart.data", "r") as f:
    headers = f.readline().strip().split(",")

feature_names = ["ldl", "adiposity", "typea", "obesity", "alcohol", "age"]
target_name = "chd"
feature_indices = [headers.index(fn) for fn in feature_names]
target_index = headers.index(target_name)

# 2) Only use first 20 samples
X = np.array([[float(row[i]) for i in feature_indices] for row in data[:20]])
y = np.array([1 if int(row[target_index]) == 1 else -1 for row in data[:20]])

# 3) SVM Dual
K = X @ X.T
P = np.outer(y, y) * K
n = X.shape[0]

def objective(alpha):
    return 0.5 * alpha @ P @ alpha - np.sum(alpha)

def svm_dual_constraint(alpha):
    return np.dot(alpha, y)

bounds = [(0, None)] * n
constraints = {"type": "eq", "fun": svm_dual_constraint}
alpha0 = np.zeros(n)

res = minimize(objective, alpha0, bounds=bounds, constraints=constraints)
alphas = res.x

# 4) Compute slope, intercept, etc.
w = ((alphas * y)[:, None] * X).sum(axis=0)
support_indices = np.where(alphas > 1e-5)[0]
b = np.mean([y[i] - np.dot(w, X[i]) for i in support_indices])

distances = (X @ w + b) / np.linalg.norm(w)
predictions = np.sign(X @ w + b)
accuracy = np.mean(predictions == y)
margin = 1.0 / np.linalg.norm(w)

x_new = np.ones(X.shape[1])  # All features=1
pred_label = np.sign(w @ x_new + b)

# 5) Print SciPy results
print("Dual variables (alphas):\n", alphas, "\n")
print("Slope vector (w):\n", w, "\n")
print("Intercept (b):\n", b, "\n")
print("Support vector indices:\n", support_indices, "\n")
print("Distances from hyperplane:\n", distances, "\n")
print("Accuracy:", accuracy, "\n")
print("Margin:", margin, "\n")
print("Prediction for x=all ones:", "CHD" if pred_label == 1 else "No CHD")


# --------------------------------------------------------
#            Scikit-learn Version
# --------------------------------------------------------
print("\n===== Output from Scikit-learn (Problem 3) =====\n")

clf = SVC(kernel="linear", C=1e10)  # approximate hard margin
clf.fit(X, y)

# (a) Reconstruct the dual variables alpha
#    scikit-learn only exposes alpha_i * y_i for SVs in clf.dual_coef_[0].
#    We place them into a length-n array, 0 for non-SVs.
alphas_skl = np.zeros(n, dtype=float)
alpha_y = clf.dual_coef_[0]        # shape: (1, n_SV)
support_indices_skl = clf.support_

for i, sv_ix in enumerate(support_indices_skl):
    alphas_skl[sv_ix] = alpha_y[i] / y[sv_ix]

w_skl = clf.coef_.ravel()
b_skl = clf.intercept_[0]
distances_skl = (X @ w_skl + b_skl) / np.linalg.norm(w_skl)
accuracy_skl = clf.score(X, y)
margin_skl = 1.0 / np.linalg.norm(w_skl)
pred_label_skl = np.sign(w_skl @ x_new + b_skl)

# Print scikit-learn results
print("Dual variables (alphas) reconstructed:\n", alphas_skl, "\n")
print("Slope vector (w):\n", w_skl, "\n")
print("Intercept (b):\n", b_skl, "\n")
print("Support vector indices:", support_indices_skl, "\n")
print("Distances from hyperplane:\n", distances_skl, "\n")
print("Accuracy:", accuracy_skl, "\n")
print("Margin:", margin_skl, "\n")
print("Prediction for x=all ones:", "CHD" if pred_label_skl == 1 else "No CHD")
