# Pages Documentation

Documentation for all of the pages.

# About | 30

## Purpose

> Provides a brief introduction to the application.

* Outlines the goal of the demo, focusing on showcasing the technology stack (like Streamlit) and platform features.
* Informs the user that more features and information are planned for future updates.

## How It Works

1.  Imports necessary libraries (`streamlit`, `streamlit_extras`, `modules.nav`).
2.  Renders the sidebar navigation links using the imported `SideBarLinks()` function.
3.  Displays the main title "# About this App" using `st.write`.
4.  Uses `st.markdown` to display the descriptive text about the app's purpose and goals.

## API Connections

* This page primarily uses [Streamlit](https://streamlit.io/) for rendering the UI components.
* It uses the custom `SideBarLinks` function from `modules.nav` for navigation.
* It uses `streamlit_extras` for potentially adding features like the app logo (`add_logo` is imported but not explicitly used in the snippet).
* No direct external API calls (like to `http://api:4000`) are made from this page.

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

1.  The page is configured to have a wide layout (`st.set_page_config(layout='wide')`)
2.  The page renders the sidebar using the `SideBarLinks()` function which was imported.
    * This allows the user to go to one of the following pages:
        * 'View all findings' (`pages/111_Findings.py`)
        * 'View all spacecraft' (`pages/112_All_Spacecraft.py`)
        * 'View missions in detail' (`pages/113_Mission_Detail.py`)
    * This is done using `st.switch_page`.

3.  The page displays a welcome message by fetching their first name from the Streamlit session state (`st.session_state.first_name`)
4.  The form (`st.form`) is shown, containing a text input field (`st.text_input`) called "Mission Name"
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

## Purpose

> Allows users to view, search, add, and update mission findings.

* Provides functionality to associate existing findings with specific missions.

## How It Works

1.  Sets page layout to wide and renders the sidebar links.
2.  Organizes functionality into two tabs: 'View' and 'Add'.
3.  Displays all findings initially fetched from the API in a dataframe (`st.dataframe`). This includes a form (`st.form`) for searching and updating.
    * Search
        * Users enter a number (`st.number_input`) which can represent either a Finding ID or a Mission ID.
        * Checkboxes (`st.checkbox`) determine whether to search by 'Finding ID' or 'Mission ID'.
        * On form submission ('Update' button):
            * If 'Search Finding ID' is checked and a valid number is entered, fetches details for that specific finding (`GET /findings/{title}`). Displays results.
            * If 'Search Mission ID' is checked and a valid number is entered, fetches all findings associated with that mission (`GET /missions/{title}/findings`). Displays results.
    * Update/Associate
        * If a Finding ID search was performed (`findingSearch` has data), input fields for 'Notes' (`st.text_input`) and 'Significance' (`st.text_input`) appear. If these fields are filled and the form is submitted, it attempts to update the finding via `PUT /findings/{title}/Notes/{findingNotes}` and/or `PUT /findings/{title}/Sig/{findingSig}`.
        * If a Mission ID search was performed (`missionSearch` has data), a number input 'FindingID Select' (`st.number_input`) appears. If a valid Finding ID (that exists in the main `data` but not already associated with the searched mission) is entered and the form submitted, it attempts to associate this finding with the mission via `POST /missions/{title}/findings/{findingSelect}`.
    * Success messages (`st.success`) are shown upon successful API responses (status code 200).
4.  Add
    * Contains a form (`st.form`) for adding new findings.
    * Input fields include:
        * 'Significance' (`st.selectbox`: Low, Medium, High)
        * 'FindingDate' (`st.date_input`)
        * 'Notes' (`st.text_input`)
    * On form submission ('Add' button):
        * Sends a `POST` request to `/findings` with the entered data in JSON format.
        * Displays success (`st.success`) or error (`st.error`) messages based on the API response. Handles potential request exceptions.

## API Connections

This page interacts many times with the local API (`http://api:4000`) using the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/findings`: Fetches all findings (used in View tab).
* `GET http://api:4000/findings/{findingID}`: Fetches details for a specific finding.
* `GET http://api:4000/missions/{missionID}/findings`: Fetches all findings associated with a specific mission.
* `PUT http://api:4000/findings/{findingID}/Notes/{notes}`: Updates the notes for a specific finding.
* `PUT http://api:4000/findings/{findingID}/Sig/{significance}`: Updates the significance for a specific finding.
* `POST http://api:4000/missions/{missionID}/findings/{findingID}`: Associates an existing finding with a mission.
* `POST http://api:4000/findings`: Adds a new finding record.

# All Spacecraft | 112

## Purpose

> Allows users to view astronauts and parts associated with a specific spacecraft.

* Displays a list of all spacecraft.
* Provides functionality to add new parts to a selected spacecraft.
* Offers navigation to the [Astronaut Data](#astronaut-data--114) page.

## How It Works

1.  Layout & Navigation: Sets page layout to wide and renders the sidebar links.
2.  Main Form (`st.form("aaa")`):
    * Fetches and displays all spacecraft data (`GET /spacecraft`) in a dataframe.
    * Provides a number input (`st.number_input`) for users to enter a `spacecraftID`.
    * Includes a checkbox (`st.checkbox`) labeled "Add Part".
    * Update Button (`st.form_submit_button('Update')`):
        * When clicked, if a valid `spacecraftID` is entered:
            * Verifies the entered `spacecraftID` exists in the fetched spacecraft data.
            * Fetches astronaut data for the ship (`GET /astronauts/onShip/{spacecraftID}`). Displays if found.
            * Fetches part data for the ship (`GET /spacecraft/{spacecraftID}/parts`). Displays if found.
    * Add Part Functionality:
        * If the "Add Part" checkbox is checked, additional fields appear within the form:
            * 'Part Name' (`st.text_input`)
            * 'Mass In Tons' (`st.number_input`)
            * 'Length in CM' (`st.number_input`)
            * 'Part Usage' (`st.text_input`)
            * An 'Add Part' submit button (`st.form_submit_button('Add Part')`) appears.
        * When the 'Add Part' button is clicked:
            * Checks if all required part fields are filled.
            * Sends a `POST` request to `/spacecraft/{spacecraftID}/parts` with the new part data.
            * Displays success (`st.success`) or error (`st.error`) messages based on the API response.
3.  Navigation Button:
    * An `st.button` labeled 'Astronaut Data/Info' allows navigation to the [`pages/114_Astronaut_Data.py` page](#astronaut-data--114) using `st.switch_page`.

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/spacecraft`: Fetches the list of all spacecraft.
* `GET http://api:4000/astronauts/onShip/{spacecraftID}`: Fetches astronauts associated with a specific spacecraft.
* `GET http://api:4000/spacecraft/{spacecraftID}/parts`: Fetches parts associated with a specific spacecraft.
* `POST http://api:4000/spacecraft/{spacecraftID}/parts`: Adds a new part record to a specific spacecraft.

# Mission Detail | 113

## Purpose

> Provides a detailed view of missions, including extended information and associated star systems/astronauts.

* Allows users to edit existing mission details or add entirely new missions.

## How It Works

1. Sets page layout to wide and renders sidebar links.
2. Organizes functionality into 'View' and 'Edit' tabs.
3. **View Tab:**
    * Contains a form (`st.form`).
    * Fetches and displays extended mission data (`GET /missions/extended`) in a dataframe.
    * Provides a number input (`st.number_input`) for `starSystemID`.
    * Update Button: When clicked with a valid `starSystemID` entered:
        * Verifies the `starSystemID` exists in the initial extended data.
        * Fetches details for that specific star system (`GET /starsystems/{starSystemID}`). Displays data.
        * Fetches astronauts associated with missions targeting that star system (`GET /astronauts/missions/{starSystemID}`). Displays data.
4.  **Edit Tab:**
    * Contains a form (`st.form("build-a-mission")`).
    * Fetches and displays the same extended mission data (`GET /missions/extended`) for reference.
    * Fetches all star system IDs (`GET /galaxies/starsystems`) to populate a dropdown.
    * Provides a selectbox (`st.selectbox`) to choose the mode: 'Update' or 'Add'.
    * Includes input fields for mission attributes:
        * 'ID' (`st.number_input`, primarily used for 'Update' mode)
        * 'MissionName' (`st.text_input`)
        * 'Objective' (`st.text_input`)
        * 'Agency' (`st.text_input`)
        * 'SuccessRating' (`st.selectbox`: High, Medium, Low)
        * 'System ID' (`st.selectbox`, populated with fetched IDs)
        * 'StartDate' (`st.date_input`)
        * 'EndDate' (`st.date_input`)
    * **Update Button:**
        * **If 'Update' mode is selected:**
            * Verifies the entered `ID` exists.
            * For each field that has a non-empty value provided, it sends a `PUT` request to the corresponding API endpoint to update that specific attribute (e.g., `PUT /missions/{ID}/name/{MissionName}`, `PUT /missions/{ID}/objective/{Objective}`, etc.).
        * **If 'Add' mode is selected:**
            * Checks if required fields (Name, Objective, Agency, Rating, SystemID, StartDate) are provided.
            * Sends a `POST` request to `/missions` with basic mission details.
            * If successful, retrieves the newly created `MissionID` by searching for the mission name (`GET /missions/name/{MissionName}`).
            * Sends a second `POST` request to `/missions/starsystem` to link the mission to the selected star system and dates.
            * Displays success or error messages for each step.
    * Includes a 'Refresh' button which likely re-runs the form logic based on current selections.

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/missions/extended`: Fetches detailed mission data (including star system info).
* `GET http://api:4000/starsystems/{starSystemID}`: Fetches details of a specific star system.
* `GET http://api:4000/astronauts/missions/{starSystemID}`: Fetches astronauts associated with missions to a specific star system.
* `GET http://api:4000/galaxies/starsystems`: Fetches star system data (likely used to get System IDs for the dropdown).
* `GET http://api:4000/missions/name/{MissionName}`: Fetches missions by name (used to get the ID after adding).
* `PUT http://api:4000/missions/{ID}/name/{MissionName}`: Updates mission name.
* `PUT http://api:4000/missions/{ID}/objective/{Objective}`: Updates mission objective.
* `PUT http://api:4000/missions/{ID}/agency/{Agency}`: Updates mission agency.
* `PUT http://api:4000/missions/{ID}/status/{SuccessRating}`: Updates mission success rating.
* `PUT http://api:4000/missions/{ID}/starsystem/{SystemID}`: Updates the target star system for a mission.
* `PUT http://api:4000/missions/{ID}/starsystem/startdate/{StartDate}`: Updates mission start date for a star system visit.
* `PUT http://api:4000/missions/{ID}/starsystem/enddate/{EndDate}`: Updates mission end date for a star system visit.
* `POST http://api:4000/missions`: Adds a new base mission record.
* `POST http://api:4000/missions/starsystem`: Links a mission to a star system with dates.

# Astronaut Data | 114

## Purpose

> Allows viewing the missions associated with a specific astronaut.

* Provides an interface for viewing, searching, adding, updating, and deleting astronaut records.

## How It Works

1.  Sets page layout to wide and renders sidebar links.
2.  Organizes functionality into 'View' and 'Edit' tabs.
3.  **View Tab:**
    * Contains a form (`st.form("aaa")`).
    * Fetches and displays all astronaut data (`GET /astronauts`) in a dataframe.
    * Provides a selectbox (`st.selectbox`) to choose the search method: 'Search by Name' or 'Search by ID'.
    * Displays either a text input (`st.text_input`) or number input (`st.number_input`) based on the search selection.
    * Update Button: When clicked with valid search input:
        * If searching by name, calls `GET /astronauts/name/"{input}"`.
        * If searching by ID, calls `GET /astronauts/{input}`.
        * Displays the search results in a dataframe.
        * For each astronaut found, fetches and displays their associated missions (`GET /astronauts/{ID}/missions`).
4.  **Edit Tab:**
    * Contains a form (`st.form("aaaa")`).
    * Fetches and displays all astronaut data (`GET /astronauts`) for reference.
    * Provides a selectbox (`st.selectbox`) to choose the action: 'Update', 'Add', or 'Delete'.
    * Includes input fields for astronaut attributes:
        * 'ID' (`st.number_input`, required for 'Update' and 'Delete')
        * 'Country' (`st.text_input`)
        * 'Years in Space' (`st.number_input`)
        * 'Name' (`st.text_input`)
    * **Commit Button:**
        * Verifies the entered `ID` exists if the action is 'Update' or 'Delete'.
        * **If 'Update' mode:**
            * For each attribute field (Country, YearsInSpace, Name) with a non-empty value, sends a `PUT` request to update that specific field (e.g., `PUT /astronauts/{ID}/country/{Country}`).
            * Displays success/error messages.
        * **If 'Delete' mode:**
            * Sends a `DELETE` request to `/astronauts/{ID}`.
            * Displays success/error messages.
        * **If 'Add' mode:**
            * Sends a `POST` request to `/astronauts` with the Name, Country, and YearsInSpace.
            * Displays success/error messages.
    * **Refresh Button:** Refreshes the form, potentially updating the displayed mode ('in update mode!', etc.) based on the selection box.

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/astronauts`: Fetches all astronaut records.
* `GET http://api:4000/astronauts/name/"{name}"`: Searches for astronauts by name.
* `GET http://api:4000/astronauts/{astroID}`: Fetches a specific astronaut by ID.
* `GET http://api:4000/astronauts/{astroID}/missions`: Fetches missions associated with a specific astronaut.
* `PUT http://api:4000/astronauts/{astroID}/country/{country}`: Updates an astronaut's country.
* `PUT http://api:4000/astronauts/{astroID}/yearsinspace/{years}`: Updates an astronaut's years in space.
* `PUT http://api:4000/astronauts/{astroID}/name/{name}`: Updates an astronaut's name.
* `POST http://api:4000/astronauts`: Adds a new astronaut record.
* `DELETE http://api:4000/astronauts/{astroID}`: Deletes an astronaut record.

# Scientist Home | 120

## Purpose

> Acts as the main landing page or dashboard for users identified as Scientists.

* Provides quick navigation links to various data management sections relevant to scientists (Galaxy, Star System, Star, Planet databases).

## How It Works

1.  **Layout & Navigation:** Sets the page layout to wide and renders the standard sidebar links using `SideBarLinks()`.
2.  **Welcome Message:** Displays a personalized welcome message using an f-string and accessing the user's first name stored in the Streamlit session state (`st.session_state.first_name`).
3.  **Navigation Buttons:**
    * Presents a series of large, primary-styled buttons (`st.button`) using `use_container_width=True` for full width.
    * Each button corresponds to a specific data section:
        * 'Access the galaxy database'
        * 'Access the star system database'
        * 'Access the star database'
        * 'Access the planet database'
    * Clicking a button triggers `st.switch_page` to navigate the user to the respective page file (e.g., `pages/121_Galaxy_Data.py`, `pages/122_Star_System_Data.py`, etc.).

## API Connections

* Uses [Streamlit](https://streamlit.io/) for UI rendering (`st.title`, `st.write`, `st.button`) and session state (`st.session_state`).
* Uses `st.switch_page` for internal application navigation.
* Imports `SideBarLinks` from `modules.nav`.
* No direct calls to the external `http://api:4000` are made from this page; its primary function is navigation.

# Galaxy Data | 121

# Star System Data | 122

# Star Data | 123

# Planet Data | 124

# Astrologist Home | 130 **(Don't write about yet)**

# Constellation Info | 131 **(Don't write about yet)**

# Find Constellation | 132 **(Don't write about yet)**