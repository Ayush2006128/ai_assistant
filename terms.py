import streamlit as st

with open("TERMS_OF_USE.md", "r") as file:
    terms_of_use = file.read()
# Display the terms of use in a Streamlit app
st.write(terms_of_use)