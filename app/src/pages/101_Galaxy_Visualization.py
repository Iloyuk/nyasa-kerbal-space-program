import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

st.header('Galaxy Visualization')
#st.write(f"### Hi, {st.session_state['first_name']}.")

data = requests.get('http://api:4000/galaxies').json()
st.dataframe(data)

with st.form("Galaxy Searcher"):
    GalaxyID = st.number_input("Search in Galaxy", value=None, step=1)
    viewStarSystem = st.checkbox("View Star System")
    viewStars = st.checkbox("View Stars")
    viewPlanets = st.checkbox("View Planets")
    update = st.form_submit_button('Update')
    if update:
        if GalaxyID:
            stars = []
            verif = False
            for a in data:
                if a['GalaxyID'] == GalaxyID:
                    verif = True
                    break
            if verif:
                systems = requests.get(f'http://api:4000/galaxies/{GalaxyID}/starsystems').json()
                if systems and viewStarSystem:
                    st.write("Star systems in planet:")
                    st.dataframe(systems)
                star = {}
                if viewStars:
                    st.write("Stars in star system:")
                for system in systems:
                    StarSysID = system['SystemID']
                    star = requests.get(f'http://api:4000/starsystems/{StarSysID}').json()
                    if star:
                        stars.append(star)
                        if viewStars:
                            st.dataframe(star)
                if viewPlanets:
                    st.write("Planets in star system:")
                    for s in stars:
                        for sta in s:
                            starID = sta['StarID']
                            planet = requests.get(
                                f'http://api:4000/galaxies/{starSystemID}/starsystems/{StarSysID}/stars/{starID}/planets').json()
                            if planet:
                                st.dataframe(planet)
