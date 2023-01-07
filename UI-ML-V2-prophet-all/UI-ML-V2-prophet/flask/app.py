import numpy
from sklearn import datasets
from flask import Flask, request
from json import JSONEncoder
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
        result=[df.to_dict('list'),y.tolist()]
        return result