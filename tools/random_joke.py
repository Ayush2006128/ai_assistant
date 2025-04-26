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
        """
        Fetches a random joke based on the specified language and category.
        
        If both language and category are provided, returns a joke matching those criteria.
        If either is missing, returns a default joke. If joke retrieval fails, returns an error message.
        
        Args:
            language: Optional language code for the joke (default: "en").
            category: Optional joke category (default: "neutral").
        
        Returns:
            A joke string or an error message if retrieval fails.
        """
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
        """
        Asynchronously executes the tool, but always raises NotImplementedError.
        
        Raises:
            NotImplementedError: Async execution is not supported for this tool.
        """
        raise NotImplementedError("This tool does not support async execution.")