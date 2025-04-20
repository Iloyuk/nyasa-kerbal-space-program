import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

data = {}
try:
    data = requests.get('http://api:4000/constellation').json()
except:
    st.write("**Important**: Could not connect to sample api, so using dummy data.")
    data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)