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

    if st.form_submit_button('Search'):
        if '/' in star or '\\' in star or len(star) == 0:
            st.error("Please enter a valid star name/id")
        else:
            data = requests.get(f'http://api:4000/planets/orbits',
                                params={"star": star}).json()
            if not data:
                st.error("Could not find star system")
            else:
                st.dataframe(data)

with st.form("lookup_planet"):
    st.write('**Lookup information on a planet**')
    planet_identifier = st.text_input("Enter planet name/id:")

    if st.form_submit_button('Search'):
        if '/' in planet_identifier or '\\' in planet_identifier or len(planet_identifier) == 0:
            st.error("Please enter a valid planet name/id")
        else:
            data = requests.get(f'http://api:4000/planets/{planet_identifier}').json()
            if not data:
                st.error("Could not find planet")
            else:
                st.dataframe(data)

with st.form("input"):
    st.write('**Add a new planet to the database**')
    planet_name = st.text_input("Planet Name:")
    planet_type = st.text_input("Planet Type:")
    mass = st.text_input("Mass:")
    num_moons = st.text_input("Num. of Moons:")
    eccentricity = st.text_input("Eccentricity:")
    inclination = st.text_input("Inclination:")

    if st.form_submit_button("Add"):
        try:
            response = requests.post('http://api:4000/planets', json={
                "PlanetName": planet_name if planet_name != "" else None,
                "PlanetType": planet_type,
                "Mass": mass if mass != "" else None,
                "NumMoons": num_moons if num_moons != "" else None,
                "Eccentricity": eccentricity if eccentricity != "" else None,
                "Inclination": inclination if inclination != "" else None
            })
            if response.status_code == 200:
                st.success("Planet added successfully!")
            else:
                st.error(response.json().get("error", "Unknown error"))
        except Exception as e:
            st.error("Could not insert data.")
            st.text(f"Details: {e}")

with st.form("update"):
    st.write('**Update a planet**')
    planet_id = st.text_input("*Planet ID to be modified:*")
    planet_name = st.text_input("Planet Name:")
    planet_type = st.text_input("Planet Type:")
    mass = st.text_input("Mass:")
    num_moons = st.text_input("Num. of Moons:")
    eccentricity = st.text_input("Eccentricity:")
    inclination = st.text_input("Inclination:")

    if st.form_submit_button("Update"):
        try:
            response = requests.put('http://api:4000/planets', json={
                "PlanetName": planet_name,
                "PlanetType": planet_type,
                "Mass": mass,
                "NumMoons": num_moons,
                "Eccentricity": eccentricity,
                "Inclination": inclination,
                "PlanetID": planet_id
            })

            if response.status_code == 200:
                result = response.json()
                if result.get('rows_affected') == 0:
                    st.warning("No planet was updated")
                else:
                    st.success("Planet updated successfully!")
            else:
                error = response.json().get("error", "Unknown error occurred.")
                st.error(f"Update failed: {error}")

        except requests.exceptions.RequestException as e:
            st.error("Could not update data.")
            st.text(f"Details: {e}")
