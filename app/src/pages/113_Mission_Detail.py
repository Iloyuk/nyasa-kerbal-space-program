import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()
st.title("Mission Info")

tab1,tab2 = st.tabs(['View','Edit'])
with tab1:
    with st.form("mission related stuff ig"):
        data = requests.get('http://api:4000/missions/extended').json()
        st.dataframe(data)
        starSystemID = st.number_input("Star System ID", step=1)
        update = st.form_submit_button('Update')
        if update:
            if starSystemID:
                for i in data:
                    if i['SystemID'] == starSystemID:
                        request = requests.get(f'http://api:4000/galaxies/starsystems/{starSystemID}').json()
                        astronaut = requests.get(f'http://api:4000/astronauts/missions/{starSystemID}').json()
                        st.dataframe(request)
                        st.dataframe(astronaut)
                        break
with tab2:
    with st.form("build-a-mission"):
        data = requests.get('http://api:4000/missions/extended').json()
        st.dataframe(data)
        selection = st.selectbox('Search',('Update', 'Add'))
        update = st.form_submit_button('Update')
        ID = st.number_input("ID",value=None, step=1)
        MissionName = st.text_input("MissionName",value=None)
        Objective = st.text_input("Objective",value=None)
        Agency = st.text_input("Agency",value=None)
        SuccessRating = st.selectbox("SuccessRating",("High","Medium","Low"))
        SystemID = st.number_input("SystemID",step=1,value=1)
        StartDate = st.date_input("StartDate", value=None)
        EndDate = st.date_input("EndDate", value=None)
        if update:
            verif = False
            for a in data:
                if a['MissionID'] == ID:
                    verif = True
                    break
            if selection == 'Update':
                if MissionName and MissionName != "": requests.put(f'http://api:4000/missions/{ID}/name/{MissionName}')
                if Objective and Objective != "": requests.put(f'http://api:4000/missions/{ID}/objective/{Objective}')
                if Agency and Agency != "": requests.put(f'http://api:4000/missions/{ID}/agency/{Agency}')
                if SuccessRating: requests.put(f'http://api:4000/missions/{ID}/status/{SuccessRating}')
                if SystemID: requests.put(f'http://api:4000/missions/{ID}/starsystem/{SystemID}')
                if StartDate: requests.put(f'http://api:4000/missions/{ID}/starsystem/startdate/{str(StartDate)}')
                if EndDate: requests.put(f'http://api:4000/missions/{ID}/starsystem/enddate/{str(EndDate)}')
            if selection == 'Add':
                try:
                    requests.post(f'http://api:4000/missions',json={
                        "MissionName":MissionName,
                        "Agency":Agency,
                        "Objective":Objective,
                        "SuccessRating": str(SuccessRating)
                    })
                    NewID = requests.get(f'http://api:4000/missions/name/{MissionName}').json()
                    for newID in NewID:
                        ID = newID['MissionID']      
                    requests.post(f'http://api:4000/missions/starsystem',json={
                        "MissionID":ID,
                        "SystemID":SystemID,
                        "StartDate":str(StartDate),
                        "EndDate":str(EndDate),
                    })
                except Exception as e:
                    st.error(f"Cannot be completed: {e}")
