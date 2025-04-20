import streamlit as st

chat_page = st.Page("chat.py", title="Chat AI Assistant", icon="🤖")
search_page = st.Page("search.py", title="Search with Tavily", icon="🔍")

router = st.navigation([chat_page, search_page])
# Set the page configuration
st.set_page_config(
    page_title="coolGemini",
    page_icon="favicon.png",
    layout="wide",
)

router.run()