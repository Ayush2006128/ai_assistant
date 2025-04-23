from langchain.tools import BaseTool
from jokeapi import Jokes
import asyncio

class RandomJokeTool(BaseTool):
    name: str = "random_joke"
    description: str = "Get a random joke. Use this tool when you need a laugh or want to lighten the mood."
    
    def _run(self, input: str) -> str:
        # Fetch a random joke
        raise NotImplementedError("This method should be overridden in subclasses.")
    
    async def _arun(self, input: str) -> str:
        # Asynchronous version of the run method
        jokeapi = await Jokes()
        joke = await jokeapi.get_joke(blacklist=["nsfw", "religious", "political", "racist", "sexist"])
        if joke['type'] == 'single':
            joke_text = joke['joke']
        else:
            joke_text = f"{joke['setup']} {joke['delivery']}"
        return joke_text

# Example usage
async def main():
    joke_tool = RandomJokeTool()
    joke = await joke_tool.arun("")
    print(f"Random Joke: {joke}")
if __name__ == "__main__":
    asyncio.run(main())