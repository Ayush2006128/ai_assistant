import streamlit as st

with open("PRIVACY_POLICY.md", "r") as file:
    privacy_policy = file.read()

# Display the privacy policy in a Streamlit app
st.write(privacy_policy)