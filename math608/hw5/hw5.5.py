import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# ----- Load data (same as before) -----
X_train_raw = np.loadtxt("khan.xtrain")
X_test_raw  = np.loadtxt("khan.xtest")
y_train     = np.loadtxt("khan.ytrain")
y_test      = np.genfromtxt("khan.ytest", missing_values="NA", filling_values=np.nan)

valid_mask = ~np.isnan(y_test)
y_test = y_test[valid_mask]
X_test_raw = X_test_raw[:, valid_mask]

X_train = X_train_raw.T
X_test  = X_test_raw.T

scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)
X_test_std  = scaler.transform(X_test)

# ---- Now we skip lambda=0, going from 0.01 to 1.0 ----
lambda_values = np.linspace(0.01, 1.0, 50)
train_acc_list = []
test_acc_list  = []

for lam in lambda_values:
    lda_model = LinearDiscriminantAnalysis(
        solver="lsqr",
        shrinkage=lam
    )
    lda_model.fit(X_train_std, y_train)
    
    y_train_pred = lda_model.predict(X_train_std)
    y_test_pred  = lda_model.predict(X_test_std)
    
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc  = accuracy_score(y_test,  y_test_pred)
    
    train_acc_list.append(train_acc)
    test_acc_list.append(test_acc)

# ---- Plot results ----
plt.plot(lambda_values, train_acc_list, label="Train")
plt.plot(lambda_values, test_acc_list,  label="Test")
plt.xlabel("Lambda")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.show()
