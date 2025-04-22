import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import logging

dotenv.load_dotenv(".env")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")  # Default model
temperature = float(os.getenv("TEMPERATURE", 0.8))  # Default temperature

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model=model_name,
    temperature=temperature,
)
# Define the tools
search_tool = TavilySearchResults(
    api_key=tavily_api_key,
    num_results=5,
)


tools = [search_tool]

react_prompt_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}] # <-- Make sure this is present
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad} # <-- Make sure this is present
"""

prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
    template=react_prompt_template
)
# Initialize the agent with the tools and prompt
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

memory = ConversationBufferMemory(memory_key="chat_history")

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    max_iterations=3,
    handle_parsing_errors=True,
)

if __name__ == "__main__":
    # Example usage
    query = "What is the capital of France?"
    logging.info(f"Query: {query}")
    response = agent_executor.invoke(input={"input": query})
    logging.info(f"Response: {response}")
