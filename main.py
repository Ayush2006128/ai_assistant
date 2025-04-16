import streamlit as st
from pages.home import home

# Run the Streamlit app
if __name__ == "__main__":
    # Set the page title and icon
    st.set_page_config(page_title="coolGemini", page_icon="favicon.png")
    home()
