import pandas as pd
import streamlit as st
from app_pages.app_page import AppPage
import pymysql

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
    connection = pymysql.connect(host="192.168.24.39", port=3306, user="mitac", passwd="mitac", db='mlflow')
    st.write("訓練紀錄")
    with st.container():
        sql_runs = '''
            select a.run_uuid, a.name, a.experiment_id, b.name exp_name from mlflow.runs a, mlflow.experiments b
            where a.experiment_id = b.experiment_id
            order by a.start_time desc
            limit 10
            '''
        df_runs = pd.read_sql(sql_runs, connection)
        radio_items = df_runs.head[['name', 'exp_name']]
        opts = []
        for j, k in df_runs.values:
            opt = j + " " + k
            opts += opt
        opts = tuple(opts)
        st.radio('選擇訓練Model', opts)

