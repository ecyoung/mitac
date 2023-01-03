
import streamlit as st
from PIL import Image
import mlflow

from app_pages.multiapp import MultiApp
from util.config_setup import config_setup
from util import pword
from util import sidabar_auth


def run():
    config_setup()

    st.set_page_config(page_title=st.session_state['lang_config']['root']['page_title'], page_icon="resources/mitac-logo.png", initial_sidebar_state='auto')  # , layout = 'wide')

    logo = Image.open(r'resources/mitac-logo.png')
    st.sidebar.image(logo, width=120)

    mlflow.set_tracking_uri('mysql://mitac:mitac@localhost:3306/mlflow')


    run_app()
    # save_users(namel)

def run_app():
# Set login widget
    namel, auth_state, username = pword.login_widget.login_feature()


    # st.title(st.session_state['prophet_df_pred_all'])

    app = MultiApp()

    from app_pages.home import HomePage
    app.add_app(HomePage)

    from app_pages.eda_pd_profiling.eda3 import EDA3Page
    app.add_app(EDA3Page)

    from app_pages.decision1 import Decision1Page
    app.add_app(Decision1Page)

    from app_pages.Classification.clf1 import CLF1Page
    app.add_app(CLF1Page)

    from app_pages.Regression.mlv2_V2 import MLV2_V2_Page
    app.add_app(MLV2_V2_Page)

    # from app_pages.PredictNextOrder.pno import PNO_Page
    # app.add_app(PNO_Page)

    from app_pages.PredictNextOrder2.pno import PNO2_Page
    app.add_app(PNO2_Page)

    from app_pages.config_page import ConfigPage
    app.add_app(ConfigPage)

    appPredict = MultiApp()
    from app_pages.predict_pages import predict_page
    appPredict.add_app(predict_page.PredictPage)

    if auth_state:
        selected = sidabar_auth.authenticat(auth_state).Sidebar_control()
        if selected == 'Train':
            app.run()

        elif selected == 'Test':
            appPredict.run()

    else:
        st.title('Please Login First')

if __name__ == '__main__':
    run()
