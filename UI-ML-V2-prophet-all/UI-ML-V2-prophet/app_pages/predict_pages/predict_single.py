import streamlit as st
from app_pages.app_page import AppPage
import pyodbc

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
    # connection = pyodbc.connect('DRIVER=MySQL ODBC 8.0 Unicode Driver;SERVER=localhost;PORT=3306;DATABASE=mitac;UID=mitac;PWD=mitac')
    col1, col2 = st.columns(2)
    with col1:
        st.write("選擇Model")

