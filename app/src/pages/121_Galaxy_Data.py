import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Galaxy information")

data = {}
try:
    data = requests.get('http://api:4001/galaxy').json()
except:
    st.write("**Important**: Could not connect to sample api.")
    data = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)