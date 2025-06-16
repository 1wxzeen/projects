import numpy as np
import matplotlib.pyplot as plt

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.covariance import ledoit_wolf

X_nci_raw_full = np.loadtxt(
    "nci.data.csv",
    delimiter=",",
    skiprows=1,
    usecols=range(1,65)
)

labels_full = np.genfromtxt(
    "nci.label.txt",
    dtype=str,
    delimiter="\n"
)

print(f"Loaded nci.data.csv with shape={X_nci_raw_full.shape}")
print(f"Loaded nci.label.txt with length={len(labels_full)}")

selected_classes = {"renal", "colon", "melanoma"}
mask = np.array([(lbl.lower() in selected_classes) for lbl in labels_full])

X_nci_filtered = X_nci_raw_full[:, mask]  
labels_filtered = labels_full[mask]

print(f"After filtering, we have shape={X_nci_filtered.shape}, labels={len(labels_filtered)}")

X_nci_110 = X_nci_filtered[:110, :] 

X_nci = X_nci_110.T  
y_nci = labels_filtered

print(f"Final data shape for LDA: X={X_nci.shape}, y={y_nci.shape}")

scaler = StandardScaler()
X_nci_std = scaler.fit_transform(X_nci)

lambda_values = np.linspace(0.01, 1.0, 40)  
loo = LeaveOneOut()

cv_accuracy_list = []

for lam in lambda_values:
    lda_model = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=lam)
    scores = cross_val_score(lda_model, X_nci_std, y_nci, cv=loo, scoring='accuracy')
    mean_score = scores.mean()
    cv_accuracy_list.append(mean_score)

plt.figure(figsize=(6,4))
plt.plot(lambda_values, cv_accuracy_list, marker='o')
plt.xlabel("Shrinkage (lambda)")
plt.ylabel("LOO-CV Accuracy")
plt.title("NCI Data (renal/colon/melanoma): LDA + LOO CV")
plt.grid(True)
plt.show()

best_lambda_cv = lambda_values[np.argmax(cv_accuracy_list)]
best_cv_acc = max(cv_accuracy_list)
print(f"Best lambda from LOO-CV: {best_lambda_cv:.3f}  (accuracy={best_cv_acc:.3f})")

lda_opt = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=best_lambda_cv)
lda_opt.fit(X_nci_std, y_nci)
y_pred_all = lda_opt.predict(X_nci_std)
final_acc = accuracy_score(y_nci, y_pred_all)

print(f"Accuracy on entire subset with best lambda: {final_acc:.3f}")

cov_estimated, lw_value = ledoit_wolf(X_nci_std)
print(f"Ledoit-Wolf shrinkage estimate = {lw_value:.3f}")
