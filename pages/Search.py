import streamlit as st
# Assume these functions exist in the specified paths and handle API calls
from logic.search_agent import search
from logic.youtube_agent import search_youtube_videos

# --- Helper Functions for Displaying Results ---

def display_answer(answer):
    """Displays the direct answer."""
    if answer:
        st.subheader("Answer")
        st.write(answer)
        st.write("---")
    else:
        st.info("No direct answer found.")

def display_images(images):
    """Displays image results, potentially in columns."""
    if images:
        st.subheader("Images")
        # Use columns for better layout, adjust number as needed
        cols = st.columns(3)
        for i, image_url in enumerate(images):
            with cols[i % 3]:
                # Add error handling for potentially broken image links
                st.image(image_url, use_column_width=True)
        st.write("---")
    else:
        st.info("No images found.")

def display_videos(videos):
    """Displays video results."""
    if videos:
        st.subheader("Videos")
        for video in videos:
            title = video.get('title', 'No Title')
            link = video.get('video_link', '#')
            thumbnail = video.get('thumbnail_url')

            st.write(f"**[{title}]({link})**")
            # Add error handling for image loading if URLs can be invalid or missing
            if thumbnail:
                try:
                    st.image(thumbnail)
                except Exception as e:
                    st.warning(f"Could not load thumbnail for '{title}'. Error: {e}")
            else:
                st.caption("No thumbnail available.")
            st.write("---")
    else:
        st.info("No videos found.")

def display_web_results(results):
    """Displays web search results."""
    if results:
        st.subheader("Web Results")
        for result in results:
            title = result.get('title', 'No Title')
            link = result.get('link', '#')
            content = result.get('content', 'No snippet available.')
            st.write(f"**[{title}]({link})**")
            st.write(content)
            st.write("---")
    else:
        st.info("No web results found.")

# --- Streamlit App Layout ---

# Set the page configuration
st.set_page_config(
    page_title="Search",
    page_icon=":mag:",
    layout="wide" # Use wide layout for better display
)

st.title("🔍 Search Engine")

# Input field for the search query
# Use session state to keep the query across reruns if needed, but simple text_input is fine for this structure
query = st.text_input("Enter your search query:", key="search_query")

# Initialize variables to store results
web_search_results = None
video_search_results = None
search_error = None

# Perform search only if a query is entered
if query:
    # Use a spinner to indicate activity during API calls
    with st.spinner("Searching across sources..."):
        try:
            # Perform all searches once using the actual imported functions
            # Ensure your 'search' function returns a dict like the mock
            # Ensure your 'search_youtube_videos' returns a list of dicts like the mock
            web_search_results = search(query) # Fetches web results and images
            video_search_results = search_youtube_videos(query)
        except Exception as e:
            # Catch potential errors during API calls (network issues, API errors, etc.)
            search_error = f"An error occurred during search: {e}"
            # Display error immediately below the search bar
            st.error(search_error)

# Create tabs
tab_titles = ["All", "Images", "Videos", "Web"]
tabs = st.tabs(tab_titles)

# --- Tab Content ---

# Tab 1: All Results
with tabs[0]:
    st.header("All Results")
    if query:
        if search_error:
            # If an error occurred during search, display it here as well
            st.error(search_error)
        # Check if either search returned results (even if one failed, the other might have succeeded)
        elif web_search_results or video_search_results:
            # Display Answer (from web search results)
            # Check if web_search_results exists and has the 'answer' key
            if web_search_results and web_search_results.get('answer'):
                 display_answer(web_search_results.get('answer'))
            else:
                 # Provide feedback if the answer specifically wasn't found or web search failed
                 if web_search_results is not None: # Check if web search ran
                     st.info("No direct answer found for this query.")

            # Display Images (from web search results)
            if web_search_results and web_search_results.get('images'):
                display_images(web_search_results.get('images'))
            else:
                 if web_search_results is not None:
                     st.info("No images found for this query.")


            # Display Videos
            if video_search_results:
                display_videos(video_search_results)
            else:
                 # Check if video search ran but returned no results vs. failed entirely
                 if not search_error: # Only show info if no major error occurred
                     st.info("No videos found for this query.")

            # Display Web Results (from web search results)
            if web_search_results and web_search_results.get('results'):
                display_web_results(web_search_results.get('results'))
            else:
                 if web_search_results is not None:
                     st.info("No web results found for this query.")

        elif not search_error: # If no error but both results are None/empty
            st.warning("No results found for your query.")
    else:
        # Prompt user to enter a query if the input is empty
        st.info("Enter a search query above to see results.")

# Tab 2: Images
with tabs[1]:
    st.header("Image Results")
    if query:
        if search_error:
            st.error(search_error) # Show general search error if it occurred
        elif web_search_results:
            # Display images if web search results are available
            display_images(web_search_results.get('images'))
        elif not search_error: # Only show warning if no general error
             st.warning("Image search could not be performed or yielded no results. Check the 'All' tab.")
    else:
        st.info("Enter a search query to see image results.")

# Tab 3: Videos
with tabs[2]:
    st.header("Video Results")
    if query:
        if search_error:
            # Show general search error if it occurred
             st.error(search_error)
        # Check specifically if video_search_results is available (it might be None even if web_search_results exists)
        elif video_search_results is not None:
             display_videos(video_search_results)
        elif not search_error: # Only show warning if no general error
             # This case handles if search_youtube_videos specifically returned None or empty list
             st.warning("Video search could not be performed or yielded no results.")
    else:
        st.info("Enter a search query to see video results.")

# Tab 4: Web Results
with tabs[3]:
    st.header("Web Results")
    if query:
        if search_error:
            st.error(search_error) # Show general search error
        elif web_search_results:
            # Display web results if available
            display_web_results(web_search_results.get('results'))
        elif not search_error: # Only show warning if no general error
             st.warning("Web search could not be performed or yielded no results. Check the 'All' tab.")
    else:
        st.info("Enter a search query to see web results.")
