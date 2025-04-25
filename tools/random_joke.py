import asyncio
from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from jokeapi import Jokes  # Assuming you have jokeapi installed (pip install jokeapi)

# Define the input schema for the tool
class JokeInput(BaseModel):
    """Input schema for the JokeAPI tool."""
    category: Optional[str] = Field(None, description="Optional category for the joke (e.g., 'Programming', 'Pun', 'Spooky'). Leave empty for any category.")
    search_string: Optional[str] = Field(None, description="Optional string to search for within the joke.")
    blacklist: Optional[str] = Field(None, description="Optional comma-separated list of flags to blacklist (e.g., 'nsfw,religious').")

class AsyncJokeTool(BaseTool):
    name: str = "async_joke_tool"
    description: str = (
        "A tool to fetch a joke from the JokeAPI asynchronously. "
        "Optionally specify a category (e.g., 'Programming', 'Pun', 'Spooky'), "
        "a search string, or a comma-separated list of blacklist flags (e.g., 'nsfw,religious')."
    )
    args_schema: Type[BaseModel] = JokeInput

    async def _arun(
        self,
        category: Optional[str] = None,
        search_string: Optional[str] = None,
        blacklist: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        try:
            j = await Jokes()

            # Prepare parameters for the jokeapi call
            params = {}
            if category:
                params['category'] = category
            if search_string:
                params['search_string'] = search_string
            if blacklist:
                params['blacklist'] = blacklist

            # Fetch the joke asynchronously
            # The get_joke method from jokeapi is already async
            joke = await j.get_joke(**params)

            if joke["error"]:
                return f"Error fetching joke: {joke['message']}"

            if joke["type"] == "single":
                return joke["joke"]
            else: # type is "twopart"
                return f"{joke['setup']}\n{joke['delivery']}"

        except Exception as e:
            return f"An error occurred: {e}"

    # Although this is an async tool, _run is required by the BaseTool interface.
    # We can raise a NotImplementedError or call the async method if needed,
    # but since the underlying library is async-only, we'll indicate it's not implemented for sync.
    def _run(
        self,
        category: Optional[str] = None,
        search_string: Optional[str] = None,
        blacklist: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool synchronously (not implemented for this async tool)."""
        raise NotImplementedError("AsyncJokeTool does not support synchronous execution.")

# Example of how to use the tool (requires an async context)
async def main():
    tool = AsyncJokeTool()
    # Example usage: Get a programming joke
    programming_joke = await tool.arun({"category": "Programming"})
    print(programming_joke)

    # Example usage: Get a joke about a chicken
    chicken_joke = await tool.arun({"search_string": "chicken"})
    print(chicken_joke)

    # Example usage: Get a joke excluding NSFW and religious flags
    clean_joke = await tool.arun({"blacklist": "nsfw,religious"})
    print(clean_joke)

if __name__ == "__main__":
    asyncio.run(main())
