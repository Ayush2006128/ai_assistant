import streamlit as st
import asyncio
from concurrent.futures import ThreadPoolExecutor
from logic.chat_agent import agent_executor
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.title("🤖 AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_agent_response(prompt):
    """Calls the agent executor's ainvoke in a separate thread and returns the response."""
    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(agent_executor.ainvoke({"input": prompt}))
            return response
        finally:
            loop.close()

    try:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(run_async)
            response = future.result()
        return response.get('output', 'Sorry, I could not find an answer.')
    except Exception as e:
        logging.info(f"Error in get_agent_response: {e}")
        return f"An error occurred: {e}"

if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            final_answer = get_agent_response(prompt)
            st.markdown(final_answer)

    st.session_state.messages.append({"role": "assistant", "content": final_answer})
