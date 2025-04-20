import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state.first_name}")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View all the constellations',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/131_Constellation_Info.py')