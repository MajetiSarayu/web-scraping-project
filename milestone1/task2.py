from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
from io import BytesIO


library_site_url = "http://publiclibraries.com/state/"

def streamlit_app():
    st.title("Library Scraper")
    st.header("Lezzgo scrape the library details!")
    states_urls = get_states_and_their_urls()
    if states_urls:
        states = list(states_urls.keys())
        selected_state = st.selectbox("select a state", states)
        

        if st.button("Scrape It!"):
            selected_state_url = states_urls[selected_state]
            dataframe = scrape_libraries(selected_state_url, selected_state)

            # Store scraped data in session state
            st.session_state['scraped_data'] = dataframe

            if dataframe is not None:
                st.success(f"Libraries scraped successfully for {selected_state}!")
        
        # Check if scraped data exists in session state and display it
        if 'scraped_data' in st.session_state:
            dataframe = st.session_state['scraped_data']
            st.dataframe(dataframe)
            csv = dataframe.to_csv()
            excel_buffer = BytesIO()
            dataframe.to_excel(excel_buffer)
            excel_buffer.seek(0)
            excel_data = excel_buffer.getvalue()
            json = dataframe.to_json()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button('Download Csv', csv, f'{selected_state}.csv')
            with col2:
                st.download_button('Download Excel', excel_data, f'{selected_state}.xlsx')
            with col3:
                st.download_button('Download Json', json, f'{selected_state}.json')
            

def get_states_and_their_urls():
    response = requests.get(library_site_url)
    if response.status_code == 200:
        contents = response.content
        soup = BeautifulSoup(contents, "html.parser")

        # getting all the state names and their library urls

        state_libraries_elements = soup.select(".dropdown > .dropdown-content > a")
        states_and_library_urls = [[state_libraries_elements[i].get_text(), state_libraries_elements[i].get("href")] 
                                        for i in range(len(state_libraries_elements))]
        if states_and_library_urls:
            states_and_urls = {}
            for i in range(len(states_and_library_urls)):
                states_and_urls[states_and_library_urls[i][0]] = states_and_library_urls[i][1]
            return states_and_urls
        else:
            print("error")

    else:
        print("404")


def scrape_libraries(url, state):

    response = requests.get(url)
    content = response.content
    if response.status_code == 200:
        soup = BeautifulSoup(content, "html.parser")

        library_details = {}
        library_row_elements = [i.select('td') for i in soup.select("#libraries tr")]
        library_row_elements = library_row_elements[1:]

        # getting library details

        library_details["city"] = [library_row_elements[i][0].get_text() for i in range(len(library_row_elements))]
        library_details["library"] = [library_row_elements[i][1].get_text() for i in range(len(library_row_elements))]
        library_details["address"] = [library_row_elements[i][2].get_text() for i in range(len(library_row_elements))]
        library_details["zip"] = [library_row_elements[i][3].get_text() for i in range(len(library_row_elements))]
        library_details["phone"] = [library_row_elements[i][4].get_text() for i in range(len(library_row_elements))]

        if library_details:
                    
            df = pd.DataFrame(library_details)
            return df

        else:
            print("Did not scrape the details successfully")

    else:
        response.raise_for_status()



streamlit_app()


