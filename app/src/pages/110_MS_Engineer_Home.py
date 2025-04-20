import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state.first_name}")
st.write('### Here is a list of all missions')

main = st.empty()

data = {}
with st.form("help"):
    title = st.text_input("Mission Name")
    data = requests.get(f'http://api:4000/missions/name/"{(title)}"').json()
    if data == []:
        data = requests.get('http://api:4000/missions/objective').json()
    st.form_submit_button('Update')
    st.dataframe(data)
    
