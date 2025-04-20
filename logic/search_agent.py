import os
import dotenv
from tavily import TavilyClient

# It's good practice to handle potential missing environment variables
dotenv.load_dotenv(".env")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in environment variables or .env file.")

# Initialize the Tavily client
client = TavilyClient(api_key=tavily_api_key)

# Define the search function
def search(query):
    """
    Search for the given query using the Tavily API and return structured results.
    """
    try:
        # Perform the search - this returns a DICTIONARY
        results_dict = client.search(
            query,
            search_depth="advanced", # Often gives better structured results
            num_results=10,
            include_answer=True,
            include_images=True,
        )

        # --- Optional: Print the raw structure for debugging ---
        # print("--- Full Tavily Response ---")
        # print(json.dumps(results_dict, indent=2))
        # print("----------------------------")
        # --- End Debugging ---

        # Extract the LIST of individual search results using .get() for safety
        individual_results_list = results_dict.get("results", [])

        # Process each individual result item from the list
        extracted_results = []
        for result_item in individual_results_list: # Iterate over the LIST
            extracted_result = {
                # Use .get() on each item dictionary for safety
                "title": result_item.get("title", "N/A"),
                "link": result_item.get("url", "N/A"),
                "content": result_item.get("content", "N/A"),
                # Note: 'answer' and 'images' are typically top-level, not per-result.
                # If Tavily *does* provide per-result images/context, adjust here.
                # Example: "score": result_item.get("score")
            }
            extracted_results.append(extracted_result)

        # Create the final structured output, including top-level info
        final_output = {
            "query": results_dict.get("query"),
            "answer": results_dict.get("answer"), # Get the main answer
            "images": results_dict.get("images", []), # Get top-level images
            "results": extracted_results # The list of processed individual results
        }

        return final_output # Return the structured dictionary

    except Exception as e:
        print(f"An error occurred during Tavily search: {e}")
        # Optional: Log the full traceback for more detailed debugging
        # import traceback
        # traceback.print_exc()
        return None

# Example usage
if __name__ == "__main__":
    query = "What is the capital of India?"
    search_output = search(query) # Renamed variable for clarity

    if search_output:
        print(f"Query: {search_output.get('query', 'N/A')}")
        print(f"Overall Answer: {search_output.get('answer', 'N/A')}") # Print the main answer
        print("-" * 20)

        # Check if the 'results' list exists and is not empty
        if search_output.get("results"):
            print("Individual Results:")
            # Iterate through the processed list within the output dictionary
            for result in search_output["results"]:
                print(f"  Title: {result.get('title', 'N/A')}")
                print(f"  Link: {result.get('link', 'N/A')}")
                print(f"  Content Snippet: {result.get('content', 'N/A')}")
                # Note: Images are handled below at the top level
                print() # Blank line between results
        else:
            print("No individual results found in the response.")

        # Print top-level images if they exist
        if search_output.get("images"):
             print(f"Top-level Images: {', '.join(search_output['images'])}")
        else:
             print("No top-level images found.")

    else:
        print("Search function failed or returned no results.")