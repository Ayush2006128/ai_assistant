from langchain_core.tools import BaseTool
import pyjokes
from pydantic import BaseModel, Field
from typing import Optional, Type
class JokeArgSchema(BaseModel):
    """Schema for joke arguments."""
    category: Optional[str] = Field(default="neutral", description="Category of the joke. Options: 'neutral', 'chuck', 'all'.")
    language: Optional[str] = Field(default="en", description="Language of the joke. Default is 'en'.")

class ProvideJoke(BaseTool):
    """Tool to provide a random joke."""
    name: str = "provide_joke"
    description: str = "Provides a random joke. You can specify the category and language."
    args_schema: Type[JokeArgSchema] = JokeArgSchema

    def _run(self, language: Optional[str] = "en", category: Optional[str] = "neutral") -> str:
        """Run the tool to get a joke."""
        if language and category:
            try:
                return pyjokes.get_joke(language=language, category=category)
            except Exception as e:
                return f"Error fetching joke: {e}"
        else:
            try:
                return pyjokes.get_joke()
            except Exception as e:
                return f"Error fetching joke: {e}"

    async def _arun(self, language: Optional[str] = None, category: Optional[str] = None) -> str:
        """Async run method for the tool."""
        raise NotImplementedError("This tool does not support async execution.")