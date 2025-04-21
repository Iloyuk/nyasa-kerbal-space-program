import logging
import streamlit as st
import requests
import json
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# Galaxy Database")

main = st.empty()

with st.form("lookup"):
    galaxy = st.text_input("Enter galaxy name for lookup:")
    st.form_submit_button('Search')
    if '/' in galaxy or '\\' in galaxy or len(galaxy) == 0:
        data = requests.get('http://api:4000/galaxies').json()
    else:
        data = requests.get(f'http://api:4000/galaxies/{galaxy}').json()
        if not data:
            data = requests.get('http://api:4000/galaxies').json()
    st.dataframe(data)

with st.form("input"):
    st.write('Add a new galaxy to the database')
    galaxy_name = st.text_input('Galaxy Name')
    redshift = st.text_input('Redshift')
    year_discovered = st.text_input('Year Discovered (YYYY-MM-DD)')
    solar_mass = st.text_input('Solar Mass in Trillions')
    dominant_element = st.text_input('Dominant Element')
    submitted = st.form_submit_button('Add')

    if submitted:
        try:
            response = requests.post('http://api:4000/galaxies', json={
                "GalaxyName": galaxy_name,
                "Redshift": redshift,
                "YearDiscovered": year_discovered,
                "SolarMassTrillions": solar_mass,
                "DominantElement": dominant_element
            })

            if response.status_code == 200:
                st.success("Galaxy inserted successfully!")
            else:
                st.error(response.json().get("error", "Unknown error"))
        except requests.exceptions.RequestException as e:
            st.error("Could not retrieve data.")
            st.text(f"Details: {e}")