import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy.stats import invgamma
from numpy.random import default_rng

file_path = "LAozone.data"

with open(file_path, "r") as f:
    lines = f.readlines()

data = []
for line in lines[1:]:  
    if line.strip():
        parts = line.strip().split(",")
        if len(parts) == 10:
            data.append([float(x) for x in parts])


data = np.array(data)

y = data[:, 0]  # ozone
wind = data[:, 2]
humidity = data[:, 3]
temp = data[:, 4]
vis = data[:, 8]

X = np.column_stack((np.ones(len(y)), wind, humidity, temp, vis))

n, d = X.shape
XtX = X.T @ X
XtX_inv = inv(XtX)
prior_mean = np.zeros(d)
prior_cov = 10 * XtX_inv

a0, b0 = 3, 1  

n_iter = 200
rng = default_rng()
w_samples = np.zeros((n_iter, d))
sigma2_samples = np.zeros(n_iter)
sigma2 = 1.0  

for i in range(n_iter):
    Vn = inv(inv(prior_cov) + XtX / sigma2)
    wn = Vn @ (X.T @ y / sigma2)
    w = rng.multivariate_normal(wn, Vn)
    
    resid = y - X @ w
    an = a0 + n / 2
    bn = b0 + 0.5 * resid.T @ resid
    sigma2 = invgamma.rvs(a=an, scale=bn, random_state=rng)
    
    w_samples[i, :] = w
    sigma2_samples[i] = sigma2

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(sigma2_samples, color="orange")
plt.title("Trace Plot of $\\sigma^2$")
plt.xlabel("Iteration")
plt.ylabel("$\\sigma^2$")

plt.subplot(1, 2, 2)
plt.plot(w_samples[:, 0], color="orange")
plt.title("Trace Plot of Intercept $w_0$")
plt.xlabel("Iteration")
plt.ylabel("Intercept $w_0$")

plt.tight_layout()
plt.show()

w_mean = np.mean(w_samples, axis=0)
sigma2_mean = np.mean(sigma2_samples)

print("Bayes Estimator of w (posterior mean):")
for i in range(d):
    print(f"w[{i}] = {w_mean[i]:.4f}")

print(f"\nBayes Estimator of σ² (posterior mean): {sigma2_mean:.4f}")
