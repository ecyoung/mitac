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
    # Show 10 training log
    st.markdown("## 訓練紀錄 ##")
    with st.container():
        sql_runs = '''
            select a.run_uuid, a.name, a.experiment_id, b.name exp_name from mlflow.runs a, mlflow.experiments b
            where a.experiment_id = b.experiment_id
            order by a.start_time desc
            limit 10
            '''
        df_runs = pd.read_sql(sql_runs, connection)
        radio_items = df_runs[['name', 'exp_name']]
        opts = []
        for j, k in radio_items.values:
            opt = j + ", ||" + k
            opts += [opt]
        opts = tuple(opts)
        selected = st.radio('選擇訓練Model', opts)

        # Show parameters and metrics after radio box select
        if selected:
            reget_name = selected.split(',')[0]
            reget_runid = df_runs[df_runs['name']==reget_name]['run_uuid'].values[0]
            with st.container():
                st.markdown('### Model參數 ###')
                subcol1, subcol2 = st.columns(2)
                # Get params
                with subcol1:
                    st.markdown('#### Parameters ####')
                    sql_params = """select a.key, a.value from mlflow.params a
                    where a.run_uuid = '""" + reget_runid + "'"
                    df_params = pd.read_sql(sql_params, connection)
                    st.write(df_params)
                # Get metrics
                with subcol2:
                    st.markdown('#### Metrics ####')
                    sql_metrics = """select a.key, a.value from mlflow.metrics a
                    where a.run_uuid = '""" + reget_runid + "'"
                    df_metrics = pd.read_sql(sql_metrics, connection)
                    st.write(df_metrics)
                if st.button('選擇'):
                    st.write('OK')