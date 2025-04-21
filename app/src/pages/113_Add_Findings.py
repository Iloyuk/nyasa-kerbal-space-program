import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

#Things to do:
# - /galaxies/{galaxyID}/starsystems
# - /missions
# - /missions/{missionID}
# - /spacecraft
# - /spacecraft/{spacecraftID}
# - /astronauts
# - /astronauts/{astronautID}
# - /spacecraft/{spacecraftID}/parts
# - /spacecraft/{spacecraftID}/parts/{partID}
# - /findings
# - /findings/{findingID}

with st.form("input"):
    st.write('Add new findings')
    sig = st.selectbox('Significance', ('Low','Medium','High'))
    findDate = st.date_input('FindingDate')
    notes= st.text_input('Notes')
    submitted = st.form_submit_button('Add')

    if submitted:
        try:
            response = requests.post('http://api:4000/findings', json={
                "Significance": sig,
                "FindingDate": str(findDate),
                "Notes": notes,
            })

            if response.status_code == 200:
                st.success("Finding inserted successfully!")
            else:
                st.error(response.json().get("error", "Unknown error"))
        except requests.exceptions.RequestException as e:
            st.error("Could not retrieve data.")
            st.text(f"Details: {e}")