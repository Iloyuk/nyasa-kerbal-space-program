import logging
import numbers
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

st.title("Findings for all missions")
def is_int(v):
      try:
        f=int(v)
      except ValueError:
        return False
      return True
#searching for specific mission
with st.form("wah"):
    data = requests.get('http://api:4000/findings').json()
    st.dataframe(data)
    title = st.text_input("Search by Name or ID")
    searchFinding = st.checkbox("Search Finding ID")
    searchMission = st.checkbox("Search Mission Name or ID")
    findingSearch = {}
    missionSearch = {}
    findingNotes = None
    findingSig = None
    if is_int(title): 
        if searchFinding:
            findingSearch = requests.get(f'http://api:4000/findings/{title}').json()
            findingNotes = st.text_input("Notes")
            findingSig = st.text_input("Significance")
        if searchMission: 
            missionSearch = requests.get(f'http://api:4000/missions/{title}/findings').json()
        if findingSearch:  st.dataframe(findingSearch)
        if searchMission: st.dataframe(missionSearch)    
    update = st.form_submit_button('Update')
    if update:
        if findingNotes != None and findingNotes != "":
            requests.put(f'http://api:4000/findings/{title}/Notes/{findingNotes}')
        if findingSig != None and findingSig != "":
            requests.put(f'http://api:4000/findings/{title}/Sig/{findingSig}')



    


