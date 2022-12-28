import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
import yaml

class login_widget():
    @staticmethod
    def login_feature():
        yaml_file = Path(__file__).parent / 'y_new.yaml'
        with yaml_file.open('rb') as f:
            _ = yaml.load(f, Loader=yaml.SafeLoader)
            # print(_['credentials'])
        authenticator = stauth.Authenticate(_['credentials'], cookie_name='theCookie', key='1234', cookie_expiry_days=10)
        name, auth_state, username = authenticator.login('login', 'sidebar')
        if auth_state:
            authenticator.logout('logout', 'sidebar')
            st.session_state['login_name'] = name
            st.title('Greetins, ' + name)
        elif auth_state == False:
            st.sidebar.error('Username/password is incorrect')
        elif auth_state == None:
            st.sidebar.warning('Login first')

        return name, auth_state, username

login_widget.login_feature()