import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

class authenticat():
    def __init__(self, auth_state):
        self.auth_state = auth_state

    def Sidebar_control(self):
        if self.auth_state == False or self.auth_state == None:
            st.stop()
        else:
            with st.sidebar:
                menu = option_menu('menu', options=['Train', 'Test'],menu_icon='bar-chart', icons=['alt', 'alt'])

        return menu