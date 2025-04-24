import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

with st.container():
    st.markdown (
        """
        The Kerbal Space Program database app was made by Jason, Davey, and Kylie. 

        It is a database app that keep tracks of galaxies, stars, star systems, and more, with the ability to update
        it and view, made with the intent of easy control and idenfiable info. 
        """
            )
    st.image("assets/faust.png", caption="This is the credits section!")
