import numpy
import pandas as pd
from sklearn import datasets
from flask import Flask, request
from json import JSONEncoder
from pymysql import connect
from pandas import read_sql
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import mlflow
from datetime import datetime, timezone, timedelta
from pathlib import Path
# from flask_jsonpify import jsonpify
import json
app = Flask(__name__)

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)



@app.route("/dataset", methods=['POST','GET'])
def dataset():
    print(len(datasets.load_diabetes(return_X_y=True)))
    if request.form['data']=='california_housing':
        df, y = datasets.fetch_california_housing(as_frame=True, return_X_y=True)
        print('y',type(y.tolist()))
        result=[df.to_dict('list'),y.tolist()]
        # print('df',df.to_dict())
        return result
    elif request.form['data']=='diabetes':
        df, y = datasets.load_diabetes(return_X_y=True, as_frame=True)
        result = [df.to_dict('list'), y.tolist()]
        return result


@app.route("/returnMethod", methods=['POST', 'GET'])
def return_method():
    user = request.form['user']
    connection = connect(host='192.168.24.39', port=3306, user='mitac', password='mitac', db='mlflow')
    # The df of runs of the user
    sql_runs = """
    select a.run_uuid id, a.name, c.name expNm from mlflow.runs a, mlflow.tags b, mlflow.experiments c
    where a.run_uuid = b.run_uuid
    and a.experiment_id = c.experiment_id
    and b.value = '""" + user + "' order by a.start_time desc"
    df_main = read_sql(sql_runs, connection)
    df_mainJ = df_main.to_json()

    # The params of all runs of the user
    sql_params = """
    select a.run_uuid, b.key, b.value from mlflow.tags a, mlflow.params b
    where a.run_uuid = b.run_uuid
    and a.value = '""" + user + "'"
    df_params = read_sql(sql_params, connection)
    df_paramsJ = df_params.to_json()

    # The metrics of all runs of the user
    sql_metrics = """
    select a.run_uuid, b.key, b.value from mlflow.tags a, mlflow.metrics b
    where a.run_uuid = b.run_uuid
    and a.value = '""" + user + "'"
    df_metrics = pd.read_sql(sql_metrics, connection)
    df_metricsJ = df_metrics.to_json()

    run_msg = [df_mainJ, df_paramsJ, df_metricsJ]
    return run_msg


@app.route('/decisiontree', methods=['GET', 'POST'])
def decisionTree():
    mlflow.set_tracking_uri('mysql://mitac:mitac@192.168.24.39/mlflow')

    params = request.form['params']
    data = request.form['data']
    user = request.form['user']
    df = pd.read_json(data, encoding='utf-8')
    X = df.drop(['MonthGrade', 'BU', 'RepCust'], axis=1)
    y = df['MonthGrade'].copy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=42)
    params1 = eval(params)
    max_depth = params1[0]
    max_leaf_nodes = params1[1]
    min_samples_split = params1[2]
    min_samples_leaf = params1[3]
    criterion = params1[4]

    dt = DecisionTreeClassifier(max_depth=max_depth, max_leaf_nodes=max_leaf_nodes, min_samples_split=min_samples_split,
                                min_samples_leaf=min_samples_leaf, criterion=criterion)
    decision_model = dt.fit(X_train, y_train)

    y_train_pred = decision_model.predict(X_train)
    y_test_pred = decision_model.predict(X_test)
    train_ACC = 100 * np.round(accuracy_score(y_train, y_train_pred), 3)
    test_ACC = 100 * np.round(accuracy_score(y_test, y_test_pred), 3)
    test_return = [train_ACC, test_ACC]

    # mlflow
    mlflow.set_experiment('聯成化Decision_Tree')
    dtparams = {'max_depth': max_depth, 'max_leaf_nodes': max_leaf_nodes, 'min_samples_split': min_samples_split,
                 'min_samples_leaf': min_samples_leaf, 'criterion': criterion}
    dtmatrics = {'train_accuracy': train_ACC, 'test_accuracy':test_ACC}
    mlflow.end_run()
    nameForRunName = str(datetime.now(timezone(timedelta(hours=8))))
    with mlflow.start_run(run_name=nameForRunName):
        mlflow.log_params(dtparams)
        mlflow.set_tag('mlflow.user', user)
        mlflow.log_metrics(dtmatrics)
        mlflow.sklearn.log_model(decision_model, 'model', registered_model_name='聯成化Desicion_Tree')

    return test_return






