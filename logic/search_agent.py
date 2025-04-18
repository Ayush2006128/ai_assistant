import os
import dotenv
import json
from tavily import TavilyClient
dotenv.load_dotenv(".env")

tavily_api_key = os.getenv("TAVILY_API_KEY")

# Initialize the Tavily client

client = TavilyClient(api_key=tavily_api_key)

# Define the search function
def search(query):
    """
    Search for the given query using the Tavily API.
    """
    try:
        # Perform the search
        results = client.search(query, num_results=5, include_answer=True, include_images=True)
        # Extract relevant information from the results
        extracted_results = []
        for result in results:
            extracted_result = {
                "title": result["title"],
                "link": result["url"],
                "answer": result["answer"],
                "content": result["content"],
                "images": [image.url for image in result["images"]]
            }
            extracted_results.append(extracted_result)
        # Return the extracted results
        return extracted_results
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
# Example usage
if __name__ == "__main__":
    query = "What is the capital of India?"
    results = search(query)
    if results:
        for result in results:
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Content: {result['content']}")
            print(f"Answer: {result['answer']}")
            print(f"Images: {', '.join(result['images'])}")
            print()
    else:
        print("No results found.")
