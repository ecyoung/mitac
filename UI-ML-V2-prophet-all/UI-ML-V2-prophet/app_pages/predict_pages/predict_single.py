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

