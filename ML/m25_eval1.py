from sklearn.datasets import load_boston
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRFRegressor

#
x, y = load_boston(return_X_y=True)

x_train, x_test, y_train, y_test = train_test_split(x,y, train_size=0.8)

model = XGBRFRegressor(n_estimators=1000, learning_rate=0.1)

model.fit(x_train, y_train, verbose=True, eval_metric="rmse",
                    eval_set = [(x_train, y_train), (x_test, y_test)])

#rmse,mae,logloss,error,auc

results = model.evals_result()
print("eval:", results)

y_pred = model.predict(x_test)
r2 = r2_score(y_test, y_pred) 
print("r2:", r2)
print("r2: %.2f%%", (r2*100.0))