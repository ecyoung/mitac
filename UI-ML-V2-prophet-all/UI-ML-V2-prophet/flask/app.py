import numpy
import pandas as pd
from sklearn import datasets
from flask import Flask, request
from json import JSONEncoder
from pymysql import connect
from pandas import read_sql
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




