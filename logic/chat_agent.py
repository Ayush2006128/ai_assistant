import os
import dotenv
import asyncio
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from tools.random_joke import AsyncJokeTool
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory

# Load environment variables from .env file
dotenv.load_dotenv(".env")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
temperature = float(os.getenv("TEMPERATURE", 0.7))

# --- Input Validation ---
if not google_api_key:
    logging.error("GOOGLE_API_KEY not found in environment variables.")
    exit(1)
if not tavily_api_key:
    logging.error("TAVILY_API_KEY not found in environment variables.")
    exit(1)

# --- LLM Initialization ---
try:
    llm = ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model=model_name,
        temperature=temperature,
        convert_system_message_to_human=True
    )
    logging.info(f"Initialized LLM: {model_name} with temperature {temperature}")
except Exception as e:
    logging.error(f"Failed to initialize LLM: {e}")
    exit(1)

# --- Tools Definition ---
try:
    search_tool = TavilySearchResults(
        max_results=3,
    )
    # Initialize the async joke tool
    joke_tool = AsyncJokeTool()
    tools = [search_tool, joke_tool]
    logging.info("Initialized TavilySearchResults and AsyncJokeTool tool.")
except Exception as e:
    logging.error(f"Failed to initialize tools: {e}")
    tools = []
    logging.warning("Continuing without tools due to initialization error.")

# --- Memory Initialization ---
memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True,
    input_key="input"
)
logging.info("Initialized ConversationSummaryMemory.")

# --- Prompt Template ---
react_prompt_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to consider the conversation history.

Previous conversation history:
{chat_history}

New input: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names", "chat_history"],
    template=react_prompt_template
)
logging.info("Created PromptTemplate.")

# --- Agent Initialization ---
try:
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    logging.info("Created ReAct agent.")
except Exception as e:
    logging.error(f"Failed to create agent: {e}")
    exit(1)

# --- Agent Executor ---
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)
logging.info("Created AgentExecutor.")

# --- Main Execution Block (Async) ---
async def main(): # Define main as an async function
    logging.info("Starting agent interaction loop.")
    print("Agent is ready. Type 'quit' to exit.")

    while True:
        try:
            query = input("You: ")
            if query.lower() == 'quit':
                logging.info("Exiting interaction loop.")
                break

            logging.info(f"User Query: {query}")

            # Invoke the agent executor asynchronously
            response = await agent_executor.ainvoke({"input": query}) # Use ainvoke and await

            output = response.get('output', 'No output found.')
            logging.info(f"Agent Response: {output}")
            print(f"Agent: {output}")

        except Exception as e:
            logging.error(f"An error occurred during agent execution: {e}", exc_info=True)
            print("Sorry, an error occurred. Please try again.")

    logging.info("Agent interaction finished.")

if __name__ == "__main__":
    asyncio.run(main()) # Run the async main function
