import streamlit as st
import asyncio
from logic.chat_agent import agent_executor

st.title("🤖 AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

async def get_agent_response(prompt):
    try:
        response = await agent_executor.ainvoke({"input": prompt})
        return response.get('output', 'Sorry, I could not find an answer.')
    except Exception as e:
        return f"An error occurred: {e}"

# React to user input
if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        # Use Streamlit's experimental async support
        final_answer = asyncio.run(get_agent_response(prompt))

    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    with st.chat_message("assistant"):
        st.markdown(final_answer)
