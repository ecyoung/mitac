# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 10:27:59 2020

@author: NBGhoshSu3
"""
import json

import mlflow
from pathlib import Path
from datetime import datetime, timezone, timedelta

from app_pages.app_page import AppPage
from six import StringIO
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from IPython.display import Image
#from sklearn.externals.six import StringIO
import pydotplus
import graphviz
import six
import sys
import requests as rq
from json import dumps
sys.modules['sklearn.externals.six'] = six


class Decision1Page(AppPage):
    @staticmethod
    def _run_page():
        app()

    @staticmethod
    def get_name():
        return st.session_state['lang_config']['decision1']['name']


def app():
    lang = st.session_state['lang_config']['decision1']
    login_user = st.session_state['login_name']

    # @st.cache(suppress_st_warning=True)
    max_depth = 5
    max_leaf_nodes = 100
    min_samples_split = 5
    min_samples_leaf = 5
    criterion = 'gini'

    def highlight_max(data, color='yellow'):
        attr = 'background-color: {}'.format(color)
        if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
            is_max = data == data.min()
            return [attr if v else '' for v in is_max]
        else:  # from .apply(axis=None)
            is_max = data == data.min().min()
            return pd.DataFrame(np.where(is_max, attr, ''), index=data.index, columns=data.columns)

    st.title(lang['title'])
    st.write(lang['selected_data'])

    # asking for file
    file_upload = st.sidebar.file_uploader(lang['upload_here'], type=['csv'], help=lang['upload_help'])
    name = 'c3'

    # smple file getting function

    c3 = Path('data/c3.csv')
    df = pd.read_csv(c3)
    paramsJ = dumps([max_depth, max_leaf_nodes, min_samples_split, min_samples_leaf, criterion])
    # Pass to flask
    passdecision = {'params': paramsJ, 'data': df.to_json(), 'user': st.session_state['log_user']}
    url = 'http://127.0.0.1:5001/decisiontree'
    decision_log = rq.post(url=url, data=passdecision)
    acc_train, acc_test = json.loads(decision_log.text)
    st.write('訓練資料準確率', acc_train)
    st.write('測試資料準確率', acc_test)
