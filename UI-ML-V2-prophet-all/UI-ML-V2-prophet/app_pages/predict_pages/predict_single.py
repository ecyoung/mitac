import pandas as pd
import streamlit as st
from app_pages.app_page import AppPage
import pymysql
import requests as rq
import json


class PredictPage(AppPage):
    @staticmethod
    def _run_page():
        app()

    @staticmethod
    def get_name():
        return 'Predict-單筆式'

    def __init__(self, testPrint):
        self.testPrint = testPrint
        st.write(testPrint)


def app():
    url_return_log = 'http://127.0.0.1:5001/returnMethod'
    # Get training history of login user
    passobj = {'user': st.session_state['log_user']}
    run_log = rq.post(url_return_log, data=passobj)
    mainJ, paramsJ, metricsJ = json.loads(run_log.text)

    # main = run names
    main = pd.read_json(mainJ)
    # select from radiobox and search from params and metrics
    with st.container():
        st.markdown("## 訓練紀錄 ##")
        main['show'] = main['name'] + ',  |' + main['expNm']
        show = tuple(main['show'])
        selected = st.radio('選擇訓練Model', show)

    if selected:
        # Get selected id
        select_name = selected.split(',')[0]
        id = main[main['name'] == select_name]['id'].values[0]
        with st.container():
            st.markdown("### Model參數 ###")
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                st.markdown("#### Parameters ####")
                params = pd.read_json(paramsJ)
                params_show = params[params['run_uuid'] == id].drop('run_uuid', axis=1)
                st.write(params_show)
            with subcol2:
                st.markdown("#### Scores ####")
                metrics = pd.read_json(metricsJ)
                metrics_show = metrics[metrics['run_uuid'] == id].drop('run_uuid', axis=1)
                st.write(metrics_show)

