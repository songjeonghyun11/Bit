import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.utils.testing import all_estimators
from sklearn.svm import SVC

#1 데이터
iris = pd.read_csv('./data/csv/iris.csv', header = 0)

x = iris.iloc[:, 0:4]
y = iris.iloc[:,4]

print(x)
print(y)

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size =0.2, random_state=6)

parameters = [
    {"C": [1, 10, 100, 1000], "kernel":["linear"]},
    {"C": [1, 10, 100, 1000], "kernel":["rbf"], "gamma":[0.001, 0.0001]},
    {"C": [1, 10, 100, 1000], "kernel":["sigmoid"], "gamma":[0.001, 0.0001]}
]

kfold = KFold(n_splits=5, shuffle=True)
model = GridSearchCV(SVC(), parameters, cv =kfold)

model.fit(x_train, y_train)

print("최적의 매개변수 : ", model.best_estimator_)
y_pred = model.predict(x_test)
print("최종 정답률 : ", accuracy_score(y_test, y_pred))





