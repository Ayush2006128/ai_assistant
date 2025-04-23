import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory
import logging

# Load environment variables from .env file
dotenv.load_dotenv(".env")

# Configure logging
# Sets up basic logging to display informational messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
# Retrieve API keys and model settings from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
# Use gemini-1.5-flash if MODEL_NAME is not set in .env
model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
# Use 0.7 if TEMPERATURE is not set in .env
temperature = float(os.getenv("TEMPERATURE", 0.7))

# --- Input Validation ---
# Check if necessary API keys are provided
if not google_api_key:
    logging.error("GOOGLE_API_KEY not found in environment variables.")
    exit(1) # Exit if Google API key is missing
if not tavily_api_key:
    logging.error("TAVILY_API_KEY not found in environment variables.")
    exit(1) # Exit if Tavily API key is missing

# --- LLM Initialization ---
# Initialize the Google Generative AI model
try:
    llm = ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model=model_name,
        temperature=temperature,
        convert_system_message_to_human=True # Important for some models
    )
    logging.info(f"Initialized LLM: {model_name} with temperature {temperature}")
except Exception as e:
    logging.error(f"Failed to initialize LLM: {e}")
    exit(1) # Exit if LLM initialization fails

# --- Tools Definition ---
# Initialize the Tavily search tool
try:
    search_tool = TavilySearchResults(
        max_results=3, # Limit search results to 3
    )
    tools = [search_tool]
    logging.info("Initialized TavilySearchResults tool.")
except Exception as e:
    logging.error(f"Failed to initialize TavilySearchResults: {e}")
    # Decide if you want to exit or continue without the tool
    tools = []
    logging.warning("Continuing without search tool due to initialization error.")


# --- Memory Initialization ---
# Initialize conversation summary memory to store chat history
# The LLM itself is used to create summaries of the conversation turns
memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history", # Key used to store and retrieve the history
    return_messages=True,     # Return history as message objects
    input_key="input"         # Specify the key for the user input
)
logging.info("Initialized ConversationSummaryMemory.")

# --- Prompt Template ---
# Define the prompt structure for the ReAct agent
# This template guides the agent on how to use tools and format its thoughts/actions.
# **Crucially, it now includes `chat_history` and uses `MessagesPlaceholder`**
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

# Create the PromptTemplate object
# Note: `chat_history` is now included in input_variables
prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names", "chat_history"],
    template=react_prompt_template
)
logging.info("Created PromptTemplate.")

# --- Agent Initialization ---
# Create the ReAct agent using the LLM, tools, and the defined prompt
try:
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    logging.info("Created ReAct agent.")
except Exception as e:
    logging.error(f"Failed to create agent: {e}")
    exit(1) # Exit if agent creation fails

# --- Agent Executor ---
# Set up the AgentExecutor to run the agent
# It manages the interaction loop, tool execution, and memory handling.
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,              # Pass the initialized memory here
    verbose=True,               # Print detailed execution steps
    max_iterations=5,           # Increase max iterations slightly
    handle_parsing_errors=True, # Attempt to recover from LLM output parsing errors
    # return_intermediate_steps=True # Uncomment to see detailed thought process
)
logging.info("Created AgentExecutor.")

# --- Main Execution Block ---
if __name__ == "__main__":
    logging.info("Starting agent interaction loop.")
    print("Agent is ready. Type 'quit' to exit.")

    while True:
        try:
            # Get user input
            query = input("You: ")
            if query.lower() == 'quit':
                logging.info("Exiting interaction loop.")
                break

            # Log the query
            logging.info(f"User Query: {query}")

            # Invoke the agent executor with the user input
            # The executor automatically handles memory loading/saving
            response = agent_executor.invoke({"input": query})

            # Log and print the response
            output = response.get('output', 'No output found.')
            logging.info(f"Agent Response: {output}")
            print(f"Agent: {output}")

            # Log current memory summary (optional, for debugging)
            # summary = memory.load_memory_variables({})
            # logging.debug(f"Current memory summary: {summary.get('chat_history')}")

        except Exception as e:
            # Log any errors during the interaction loop
            logging.error(f"An error occurred during agent execution: {e}", exc_info=True)
            print("Sorry, an error occurred. Please try again.")

    logging.info("Agent interaction finished.")
