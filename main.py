import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain.agents import create_react_agent, AgentType, AgentExecutor
from langchain.prompts import PromptTemplate
import streamlit as st

# Load environment variables from .env file
# Make sure to create a .env file with your API keys
# GOOGLE_API_KEY and TAVILY_API_KEY
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

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=2,
    handle_parsing_errors=True,
)
# This function sets up the Streamlit UI for the assistant
def ui():
    st.set_page_config(page_title="coolGemini", page_icon=":robot_face:")

    st.title("Google Gemini Assistant")
    st.write("Ask me anything!")
    user_input = st.text_input("Your question:")
    if st.button("Submit"):
        if user_input:
            with st.spinner("Thinking..."):
                response = agent_executor.invoke({"input": user_input})
                st.write(f"Assistant: {response}")
        else:
            st.warning("Please enter a question.")

# Command-line interface
def cli():
    while True:
        user_input = input("Ask me anything: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.run(user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    ui()
