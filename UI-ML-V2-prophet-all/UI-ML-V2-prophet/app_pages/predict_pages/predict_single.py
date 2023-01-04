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
    st.write('OK')
    connection = pymysql.connect(host="127.0.0.1", port=3306, user="mitac", passwd="mitac", db='mlflow')
    col1, col2 = st.columns(2)
    with col1:
        st.write("選擇Model")


