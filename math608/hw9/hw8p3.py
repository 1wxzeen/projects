import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon

rng = np.random.default_rng()
lambda_param = 2  
scale_param = 1 / lambda_param

# ------------------------
# Part A – NumPy's .exponential()
# ------------------------

sample_30_a = rng.exponential(scale=scale_param, size=30)
sorted_a = np.sort(sample_30_a)
sample_cdf_a = np.arange(1, 31) / 30
x_vals = np.linspace(0, 3, 300)
theoretical_cdf = expon.cdf(x_vals, scale=scale_param)

plt.figure(figsize=(8, 5))
plt.plot(x_vals, theoretical_cdf, label="Theoretical CDF", color="black")
plt.step(sorted_a, sample_cdf_a, label="Sample CDF (Part A)", color="blue", where="post")
plt.title("Part A: Sample vs Theoretical CDF (n = 30)")
plt.xlabel("x")
plt.ylabel("CDF")
plt.legend()
plt.grid(True)
plt.show()

sample_sizes = np.arange(1, 1501)
max_diffs_a = []
for n in sample_sizes:
    s = rng.exponential(scale=scale_param, size=n)
    sorted_s = np.sort(s)
    sample_cdf = np.arange(1, n+1) / n
    true_cdf = expon.cdf(sorted_s, scale=scale_param)
    max_diffs_a.append(np.max(np.abs(sample_cdf - true_cdf)))

plt.figure(figsize=(8, 5))
plt.plot(sample_sizes, max_diffs_a, color="purple")
plt.title("Part A: Max |Sample CDF - Theoretical CDF| vs Sample Size")
plt.xlabel("Sample size")
plt.ylabel("Max absolute difference")
plt.grid(True)
plt.show()


# ------------------------
# Pat B – Manual Inverse CDF Sampling
# ------------------------

def inverse_exponential(u, lam):
    return -np.log(1 - u) / lam

u_30 = rng.random(30)
sample_30_b = inverse_exponential(u_30, lambda_param)
sorted_b = np.sort(sample_30_b)
sample_cdf_b = np.arange(1, 31) / 30

plt.figure(figsize=(8, 5))
plt.plot(x_vals, theoretical_cdf, label="Theoretical CDF", color="black")
plt.step(sorted_b, sample_cdf_b, label="Sample CDF (Part B, Inverse)", color="green", where="post")
plt.title("Part B: Inverse Method Sample vs Theoretical CDF (n = 30)")
plt.xlabel("x")
plt.ylabel("CDF")
plt.legend()
plt.grid(True)
plt.show()

max_diffs_b = []
for n in sample_sizes:
    u = rng.random(n)
    samp = inverse_exponential(u, lambda_param)
    sorted_s = np.sort(samp)
    sample_cdf = np.arange(1, n+1) / n
    true_cdf = expon.cdf(sorted_s, scale=scale_param)
    max_diffs_b.append(np.max(np.abs(sample_cdf - true_cdf)))

plt.figure(figsize=(8, 5))
plt.plot(sample_sizes, max_diffs_b, color="darkgreen")
plt.title("Part B: Max |Sample CDF - Theoretical CDF| vs Sample Size (Inverse Method)")
plt.xlabel("Sample size")
plt.ylabel("Max absolute difference")
plt.grid(True)
plt.show()
