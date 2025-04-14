import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
import streamlit as st

# Load environment variables from .env file
# Make sure to create a .env file with your API keys
# GOOGLE_API_KEY and TAVILY_API_KEY
dotenv.load_dotenv(".env")

google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

llm = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model="gemini-2.0-flash",
    temperature=0.8,
)
search_tool = TavilySearchResults(
    api_key=tavily_api_key,
    num_results=5,
)

prompt = PromptTemplate(
    input_variables=["input"],
    template="You are a helpful assistant. Answer the question: {input}",
)
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=2,
)
# Streamlit app
def ui():
    st.title("Google Gemini Assistant")
    st.write("Ask me anything!")
    user_input = st.text_input("Your question:")
    if st.button("Submit"):
        if user_input:
            with st.spinner("Thinking..."):
                response = agent.run(user_input)
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