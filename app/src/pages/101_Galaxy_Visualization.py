import logging
import streamlit as st
from modules.nav import SideBarLinks
logger = logging.getLogger(__name__)

SideBarLinks()

st.header('Galaxy Visualization')
st.write(f"### Hi, {st.session_state['first_name']}.")