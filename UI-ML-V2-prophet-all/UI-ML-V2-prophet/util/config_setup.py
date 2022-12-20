
from os import listdir
from os.path import isfile, join
import json
import streamlit as st
from urllib.request import urlopen

config_folder = 'https://raw.githubusercontent.com/violentzone/mitac/20221219/UI-ML-V2-prophet-all/UI-ML-V2-prophet/config/config.json'
response = urlopen('config_folder')



def config_setup():
    if 'config' in st.session_state:
        return
    j = json.load(response)
    st.session_state['config'] = j
    set_lang(st.session_state['config']['selected_lang'], True)


def set_lang(lang, set_default=False):
    lang_files = get_lang_files()
    if lang not in lang_files:
        if not set_default:
            return
        else:
            lang = lang_files[0]
    st.session_state['current_lang'] = lang
    file = f'{lang_folder}/{lang}.json'
    with open(file, encoding='utf-8') as f:
        j = json.load(f)
    st.session_state['lang_config'] = j
    st.session_state['config']['selected_lang'] = lang
    save_config()


def save_config():
    j = json.dumps(st.session_state['config'], indent=4)
    if len(j) < 2:
        return
    with open(config_filepath, 'w', encoding='utf-8') as f:
        f.write(j)


def get_lang_files():
    return [f.replace('.json', '') for f in listdir(lang_folder) if isfile(join(lang_folder, f))]


