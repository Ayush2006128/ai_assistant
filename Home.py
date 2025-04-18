import streamlit as st
from logic.chat_agent import agent_executor

def home():
    """
    This function sets up a Streamlit chat UI for the assistant.
    """
    st.title("Google Gemini Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What's up?"):
        # Display user message in chat message container
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.spinner("Thinking..."):
            try:
                response = agent_executor.invoke({"input": prompt})
                final_answer = response.get('output', 'Sorry, I could not find an answer.')
            except Exception as e:
                final_answer = f"An error occurred: {e}"

        # Display assistant response in chat message container
        st.session_state.messages.append({"role": "assistant", "content": final_answer})
        with st.chat_message("assistant"):
            st.markdown(final_answer)

if __name__ == "__main__":
    home()