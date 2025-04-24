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
        it and view, made with the intent of easy control and identifiable info. 
        """
            )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("assets/faust.png", width=270, caption="hello! - davey")

    with col2:
        st.image("assets/skye.png", width=256, caption="sammy killed my will to live - jason")

    with col3:
        st.image("assets/nug.png", width=272, caption="dino nuggiez are yummy - kylie")
