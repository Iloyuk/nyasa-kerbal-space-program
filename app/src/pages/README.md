# `pages` Folder

This folder contains all the pages that will be part of the application. Details on required numbers will be provided in the Phase 3 documentation.

These pages are meant to show you an example of some of the features of Streamlit and the way we will limit functionality access by role/persona. It is not meant to represent a complete application.

TODO: Describe the pages folder and include link to documentation. Don't forget about ordering of pages.

(not pages 100,101,130,131,132)

# About | 30

## Purpose

## How It Works

## API Connections

# Student Home | 100 **(Don't write about yet)**



# Galaxy Visualization | 101 **(Don't write about yet)**

# MS Engineer Home | 110

## Purpose

> This page functions as a dashboard providing a quick overview of missions and serving as a launchpad to explore more specific data related to space exploration activities managed within the application.

* The home page for engineers on the platform.
* Displays the mission overview.
* Allows for mission searching/filtering.
    * It includes a form (`st.form`) where users can input a mission name to search for specific missions. The page then interacts with the backend API (`http://api:4000/missions/...`) to fetch and display data for the matching mission(s). If the search is invalid or yields no results, it falls back to fetching a default list.
* Allows users to navigate around the platform using buttons made with (`st.button`)

## How It Works

1. The page is configured to have a wide layout (`st.set_page_config(layout='wide')`)
2. The page renders the sidebar using the `SideBarLinks()` function which was imported.
    * This allows the user to go to one of the following pages:
        * 'View all findings' (`pages/111_Findings.py`)
        * 'View all spacecraft' (`pages/112_All_Spacecraft.py`)
        * 'View missions in detail' (`pages/113_Mission_Detail.py`)
    * This is done using `st.switch_page`.

3. The page displays a welcome message by fetching their first name from the Streamlit session state (`st.session_state.first_name`)
4. The form (`st.form`) is shown, containing a text input field (`st.text_input`) called "Mission Name"
    * When the user clicks the 'Update' button (`st.form_submit_button`) within the form:
        * The script checks the text that was entered in the "Mission Name" field.
        * Upon receiving invalid input the default mission list is shown.
            * `http://api:4000/missions/objective`
        * If the input contains a valid name, it attempts to fetch missions matching that specific name via the API.
            * `http://api:4000/missions/name/{title}`
        * If the name-specific search returns no data, it falls back to fetching the default list.
        * The data retrieved from the API (expected to be in JSON format) is then rendered into an interactive table using `st.dataframe`.

## API Connections

This page uses the application's local API (`http://api:4000`) as well as [Streamlit](https://streamlit.io/) and [Requests](https://pypi.org/project/requests/).


### Endpoints Used on This Page:

* `GET http://api:4000/missions/objective`: Called when the mission name search input is empty, invalid, or when a name-specific search returns no results. It gets a default list of missions
* `GET http://api:4000/missions/name/{title}`: Called when a user submits a valid mission name in the search form. `{title}` is replaced with the user's input. It retrieves missions matching that specific name.

# Findings | 111

# All Spacecraft | 112

# Mission Detail | 113

# Astronaut Data | 114

# Scientist Home | 120

# Galaxy Data | 121

# Star System Data | 122

# Star Data | 123

# Planet Data | 124

# Astrologist Home | 130 **(Don't write about yet)**

# Constellation Info | 131 **(Don't write about yet)**

# Find Constellation | 132 **(Don't write about yet)**