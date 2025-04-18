import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.header('Galaxy Visualization')
st.write(f"### Hi, {st.session_state['first_name']}.")