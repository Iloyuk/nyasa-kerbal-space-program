import logging
import streamlit as st
import requests
import json
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# Planet Database")

with st.form("lookup_star"):
    st.write('**Search a star\'s orbits**')
    star = st.text_input("Enter star name/id:")
    submitted = st.form_submit_button('Search')

    if submitted:
        if '/' in star or '\\' in star or len(star) == 0:
            st.error("Please enter a valid star name/id")
        else:
            data = requests.get(f'http://api:4000/planet/orbits',
                                params={"star": star}).json()
            if not data:
                st.error("Could not find star system")
            else:
                st.dataframe(data)

with st.form("lookup_planet"):
    st.write('**Lookup information on a planet**')
    planet_identifier = st.text_input("Enter planet name/id:")
    submitted = st.form_submit_button('Search')

    if submitted:
        if '/' in planet_identifier or '\\' in planet_identifier or len(planet_identifier) == 0:
            st.error("Please enter a valid planet name/id")
        else:
            data = requests.get(f'http://api:4000/planet/{planet_identifier}').json()
            if not data:
                st.error("Could not find planet")
            else:
                st.dataframe(data)