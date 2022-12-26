import pickle
import streamlit_authenticator as stauth
from pathlib import Path

name = ['YinChen', 'LeoChen']
userName = ['YC', 'LC']
password = ['1234', '1234']

hashed = stauth.Hasher(password).generate()

hashedFile = Path(__file__).parent/"hashed_psw.pkl"
with hashedFile.open('wb') as file:
    pickle.dump(hashed, file)