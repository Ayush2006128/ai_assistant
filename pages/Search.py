import streamlit as st
from logic.search_agent import search
from logic.youtube_agent import search_youtube_videos

# Set the page configuration
st.set_page_config(
    page_title="Search",
    page_icon=":mag:",
    layout="wide",
)

st.title("Search")

query = st.text_input("Enter your search query:")

tabs = st.tabs(["Web", "Images", "Videos", "News"])
with tabs[0]:
    if query:
        search_results = search(query)

        if search_results:
            if search_results.get('answer'):
                st.subheader("Answer:")
                st.write(search_results['answer'])
                st.write("---")
            else:
                st.error("No answer found.")

            if search_results.get('images'):
                st.subheader("Images:")
                for image_url in search_results['images']:
                    st.image(image_url)
                st.write("---")
            else:
                st.error("No images found.")
                
            if search_results.get('results'):
                st.subheader("Search Results:")
                for result in search_results['results']:
                    st.write(f"**[{result['title']}]({result['link']})**")
                    st.write(result['content'])
                    st.error("---")
            else:
                st.error("No results found.")
        else:
            st.error("An error occurred during the search.")
    else:
        st.warning("Please enter a search query to get started.")

with tabs[1]:
    if search_results.get('images'):
        st.subheader("Images:")
        for image_url in search_results['images']:
            st.image(image_url)
        st.write("---")
    else:
        st.error("No images found.")

with tabs[2]:
    video_results = search_youtube_videos(query)
    if video_results:
        st.subheader("Videos:")
        for video in video_results:
            st.write(f"**[{video['title']}]({video['video_link']})**")
            st.image(video['thumbnail_url'])
            st.write("---")
    else:
        st.error("No videos found.")

with tabs[3]:
    if search_results.get('results'):
        st.subheader("Web Results:")
        for result in search_results['results']:
            st.write(f"**[{result['title']}]({result['link']})**")
            st.write(result['content'])
            st.write("---")
    else:
        st.error("No results found.")