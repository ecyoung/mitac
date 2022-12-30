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
def hello():
    print(len(datasets.load_diabetes(return_X_y=True)))
    if request.form['data']=='california_housing':
        return json.dumps(datasets.fetch_california_housing( return_X_y=True), cls=NumpyArrayEncoder)
    if request.form['data']=='diabetes':
        return json.dumps(datasets.load_diabetes(return_X_y=True), cls=NumpyArrayEncoder)