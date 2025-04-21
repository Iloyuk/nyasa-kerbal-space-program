import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("All known spacecraft")
data = requests.get('http://api:4000/spacecraft').json()
st.dataframe(data)

#add view status
# somethign
