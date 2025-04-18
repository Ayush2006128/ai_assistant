import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

dotenv.load_dotenv(".env")

google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model="gemini-2.0-flash",
    temperature=0.8,
)
# Define the tools
search_tool = TavilySearchResults(
    api_key=tavily_api_key,
    num_results=5,
)

tools = [search_tool]

# Define the prompt template
# This is a simple prompt template that can be customized
# to include more context or instructions for the assistant.

react_prompt_template = """
Answer the following questions as best you can. You have access to the following tools:

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

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    max_iterations=2,
    handle_parsing_errors=True,
)
