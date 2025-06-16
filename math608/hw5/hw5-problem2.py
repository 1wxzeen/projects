import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

X_train_full = np.loadtxt("khan.xtrain")  # shape ~ (genes, 63)
y_train_full = np.loadtxt("khan.ytrain")  # shape ~ (63,)

X_test_full  = np.loadtxt("khan.xtest")   # shape ~ (genes, 25)
y_test_full  = np.genfromtxt("khan.ytest", missing_values="NA", filling_values=np.nan)

X_train_raw = X_train_full[:100, :]  # shape (100, 63)
X_test_raw  = X_test_full[:100, :]   # shape (100, 25)

y_train = y_train_full               # shape (63,)
X_test_raw = X_test_raw[:, -12:]     # shape now (100, 12)
y_test     = y_test_full[-12:]       # shape now (12,)

valid_mask = ~np.isnan(y_test)
y_test = y_test[valid_mask]
X_test_raw = X_test_raw[:, valid_mask]

X_train = X_train_raw.T  # shape (63, 100)
X_test  = X_test_raw.T   # shape (? , 100)

scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)
X_test_std  = scaler.transform(X_test)


lambda_values = np.linspace(0.0, 1.0, 50, endpoint=False)[1:]  

train_acc_list = []
test_acc_list  = []

for lam in lambda_values:
    lda_model = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=lam)
    lda_model.fit(X_train_std, y_train)
    
    y_train_pred = lda_model.predict(X_train_std)
    y_test_pred  = lda_model.predict(X_test_std)
    
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc  = accuracy_score(y_test,  y_test_pred)
    
    train_acc_list.append(train_acc)
    test_acc_list.append(test_acc)


best_lambda_train = lambda_values[np.argmax(train_acc_list)]
best_lambda_test  = lambda_values[np.argmax(test_acc_list)]
print("Best lambda (TRAIN):", best_lambda_train)
print("Best lambda (TEST) :", best_lambda_test)

plt.figure()
plt.plot(lambda_values, train_acc_list, label="Train Accuracy")
plt.plot(lambda_values, test_acc_list,  label="Test Accuracy")
plt.xlabel("Shrinkage (lambda)")
plt.ylabel("Accuracy")
plt.title("SRBCT (first 100 genes) - LDA with solver='lsqr'")
plt.legend()
plt.grid(True)
plt.show()

lda_opt = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=best_lambda_test)
lda_opt.fit(X_train_std, y_train)

X_zero = np.zeros((1, 100))  
X_zero_std = scaler.transform(X_zero)
pred_zero = lda_opt.predict(X_zero_std)
print(f"Prediction for all-zero features = {pred_zero[0]}")
