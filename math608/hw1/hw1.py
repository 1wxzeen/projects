import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_path = "LAozone.data"
df = pd.read_csv(file_path, delimiter=",")

df.columns = ["ozone", "vh", "wind", "humidity", "temp", "ibh", "dpg", "ibt", "vis", "doy"]

df = df[["ozone", "wind", "humidity", "temp", "vis"]].dropna()
df = df.apply(pd.to_numeric, errors='coerce')

X = df[["wind", "humidity", "temp", "vis"]].values
y = df["ozone"].values

X = np.c_[np.ones(X.shape[0]), X]  # Add intercept column

beta = np.linalg.inv(X.T @ X) @ X.T @ y  # Compute least squares estimate

y_pred = X @ beta  # Predicted values
residuals = y - y_pred  # Compute residuals

# Plot residuals
plt.figure(figsize=(8, 6))
plt.scatter(y_pred, residuals, color="orange", alpha=0.7)
plt.axhline(y=0, color="red", linestyle="--")
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()

# Predict ozone for given values
new_data = np.array([1, 5, 60, 50, 200])  # Include intercept term
predicted_ozone = new_data @ beta  # Compute prediction

# Print results
print("Intercept:", beta[0])
print("Slope for Wind:", beta[1])
print("Residuals (first 5 values):", residuals[:5])
print("Predicted Ozone for Wind=5, Humidity=60, Temp=50, Vis=200:", predicted_ozone)

