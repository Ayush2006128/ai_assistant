import os
import dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables from .env file
dotenv.load_dotenv(".env")

# Get the YouTube API key from environment variables
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
if youtube_api_key is None:
    raise ValueError("YOUTUBE_API_KEY is not set in the .env file.")

# --- Function to Search Videos ---
def search_youtube_videos(query: str, api_key=youtube_api_key, max_results: int = 10) -> list[dict]:
    """
    Searches for YouTube videos based on a query string using the YouTube Data API v3.

    Args:
        api_key: Your YouTube Data API v3 key.
        query: The search term (e.g., "python tutorial").
        max_results: The maximum number of search results to return (default is 10).

    Returns:
        A list of dictionaries, where each dictionary contains the 'title',
        'thumbnail_url', and 'video_link' of a found video.
        Returns an empty list if no videos are found or an API error occurs.
    """
    results = []
    try:
        # Build the YouTube API service object
        # You might need to install the library: pip install google-api-python-client
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Create a request to the search().list endpoint
        request = youtube.search().list(
            part="snippet",         # We need snippet for title and thumbnails
            q=query,                # The search query
            type="video",           # Only search for videos
            maxResults=max_results, # Maximum number of results
            # Optional: Specify fields to reduce response size
            fields="items(id/videoId,snippet(title,thumbnails/default/url))"
        )

        # Execute the request
        response = request.execute()

        # Process the search results
        for item in response.get('items', []):
            video_id = item.get('id', {}).get('videoId')
            snippet = item.get('snippet', {})
            title = snippet.get('title')
            thumbnail_info = snippet.get('thumbnails', {}).get('default', {})
            thumbnail_url = thumbnail_info.get('url')

            if video_id and title and thumbnail_url:
                video_link = f"https://www.youtube.com/watch?v={video_id}"
                results.append({
                    'title': title,
                    'thumbnail_url': thumbnail_url,
                    'video_link': video_link,
                })

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        # Consider more specific error handling or logging
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Consider more specific error handling or logging

    return results

# --- Example Usage ---
if __name__ == "__main__":
    # Make sure you have set YOUTUBE_API_KEY in your .env file
    # and have installed the library: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2

    search_query = "python tutorial for beginners"
    number_of_results = 5 # Ask for 5 results

    print(f"Searching YouTube for: '{search_query}' (max {number_of_results} results)")
    videos = search_youtube_videos(search_query, max_results=number_of_results)

    if videos:
        print(f"\n--- Found {len(videos)} Videos ---")
        for i, video in enumerate(videos, 1):
            print(f"\nResult {i}:")
            print(f"  Title: {video['title']}")
            print(f"  Thumbnail: {video['thumbnail_url']}")
            print(f"  Link: {video['video_link']}")
        print("--------------------")
    else:
        print(f"\nNo videos found for query: '{search_query}'")
