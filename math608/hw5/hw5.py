import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# 1) LOAD DATA
# We'll assume the files are in the same directory as this script,
# and that X_{train,test} are shaped (genes, samples) in the raw text.
# y_{train,test} are shaped (samples,).
#
# 'NA' in khan.ytest is handled by np.genfromtxt, turning them into NaN.
# ---------------------------------------------------------------------
X_train_raw = np.loadtxt("khan.xtrain")
X_test_raw  = np.loadtxt("khan.xtest")

y_train = np.loadtxt("khan.ytrain")
y_test  = np.genfromtxt("khan.ytest", missing_values="NA", filling_values=np.nan)

# ---------------------------------------------------------------------
# 2) FILTER OUT ANY 'NA' (i.e., NaN) LABELS IN y_test
# We do this by creating a mask of valid (non-NaN) labels,
# then selecting only the corresponding columns from X_test_raw
# (since X_test_raw is shaped (genes, samples)).
# ---------------------------------------------------------------------
valid_mask = ~np.isnan(y_test)
y_test = y_test[valid_mask]
X_test_raw = X_test_raw[:, valid_mask]  

# ---------------------------------------------------------------------
# 3) TRANSPOSE FEATURE MATRICES TO (#samples, #genes):
# Some algorithms (like scikit-learn) expect rows = samples, cols = features.
# ---------------------------------------------------------------------
X_train = X_train_raw.T  # shape: (#samples_train, #genes)
X_test  = X_test_raw.T   # shape: (#samples_test, #genes)

# ---------------------------------------------------------------------
# 4) SET UP THE LOOP OVER LAMBDAS
# scikit-learn's 'C' parameter = 1/lambda for L2-regularized logistic regression.
# E.g., if you want lambda in [0.01, 0.1, 1, 10, 100], then C = 1/lambda.
# ---------------------------------------------------------------------
lambda_values = [0.01, 0.1, 1, 10, 100]
train_acc_list = []
test_acc_list = []

for lam in lambda_values:
    # Create logistic regression model with L2 penalty
    model = LogisticRegression(
        penalty="l2",
        C=1.0/lam,         # 1/lambda
        solver="lbfgs",
        multi_class="multinomial",
        max_iter=5000      # Increase iterations if needed
    )
    
    # 5) FIT THE MODEL
    model.fit(X_train, y_train)
    
    # 6) PREDICT
    y_train_pred = model.predict(X_train)
    y_test_pred  = model.predict(X_test)
    
    # 7) COMPUTE & STORE ACCURACIES
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc  = accuracy_score(y_test,  y_test_pred)
    
    train_acc_list.append(train_acc)
    test_acc_list.append(test_acc)
    
    print(f"Lambda={lam:6.3f} | Train Acc={train_acc:.3f} | Test Acc={test_acc:.3f}")

# ---------------------------------------------------------------------
# 8) OPTIONAL: PLOT THE ACCURACIES vs. LAMBDA
# ---------------------------------------------------------------------
plt.plot(lambda_values, train_acc_list, label="Train Accuracy")
plt.plot(lambda_values, test_acc_list, label="Test Accuracy")
plt.xlabel("Lambda")
plt.ylabel("Accuracy")
plt.title("Logistic Regression Accuracy vs. Lambda (SRBCT Data)")
plt.legend()
plt.show()
