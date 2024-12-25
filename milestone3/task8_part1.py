# graphical user interface without any functionalities

import streamlit as st
from streamlit_tags import st_tags

def ui():
    st.set_page_config(layout="wide", page_title="Universal Web Scraper")

    with st.sidebar:
        st.markdown("### Web Scraper Settings")
        
        model = st.selectbox("Select Model", ["gpt", "gemini flash"])
        
        url = st.text_input("Enter URL")
        
        fields = st_tags(
        label="Enter Fields to Extract:",
        text="Press enter to add more",
        suggestions=["name", "email", "address", "phone"],
        maxtags=10,
        key="1")
        st.divider()
        
        if st.button("Scrape"):
            pass
    st.markdown("<h1 style='text-align: center;'>Universal Web Scraper 🦑</h1>", unsafe_allow_html=True)
ui()