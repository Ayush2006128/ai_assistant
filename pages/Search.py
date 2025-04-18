import streamlit as st
from logic.search_agent import search

# Set the page configuration
st.set_page_config(
    page_title="Tavily Search",
    page_icon=":search:",
    layout="wide",
)

st.title("Search")

query = st.text_input("Enter your search query:")

if query:
    search_results = search(query)

    if search_results:
        if search_results.get('answer'):
            st.subheader("Answer:")
            st.write(search_results['answer'])
            st.write("---")

        if search_results.get('images'):
            st.subheader("Images:")
            for image_url in search_results['images']:
                st.image(image_url)
            st.write("---")

        if search_results.get('results'):
            st.subheader("Search Results:")
            for result in search_results['results']:
                st.write(f"**[{result['title']}]({result['link']})**")
                st.write(result['content'])
                st.write("---")
        else:
            st.write("No results found.")
    else:
        st.write("An error occurred during the search.")