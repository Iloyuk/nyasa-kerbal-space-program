import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()


st.title("Spacecraft")
with st.form("aaa"):
    data = requests.get('http://api:4000/spacecraft').json()
    st.dataframe(data)
    spacecraftID = st.number_input('Insert SpacecraftID', value=None, step=1)
    update = st.form_submit_button('Update')
    if update:
        if spacecraftID:
            astronautData = requests.get(f'http://api:4000/astronauts/onShip/{spacecraftID}').json()
            partData = requests.get(f'http://api:4000/spacecraft/{spacecraftID}/parts').json()
            st.dataframe(astronautData)
            st.dataframe(partData)
            b = True
            for sc in data:
                if sc['ShipID'] == spacecraftID:
                    b = False
            if b:
                st.error("ID not in Table")
if st.button('Astronaut Data/Info',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/115_Astronaut_Data.py')