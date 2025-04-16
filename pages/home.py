import streamlit as st
from logic.agent import agent_executor

def home():
    """
    This function sets up the Streamlit UI for the assistant.
    It includes a title, a text input for the user to ask questions,
    and a button to submit the question.
    """
    st.title("Google Gemini Assistant")
    st.write("Ask me anything!")
    user_input = st.text_input("Your question:")
    if st.button("Submit"):
        if user_input:
            with st.spinner("Thinking..."):
                try:
                    response = agent_executor.invoke({"input": user_input})
                    # Access the 'output' key for the final answer
                    final_answer = response.get('output', 'Sorry, I could not find an answer.') # Use .get for safety
                    st.write("Assistant:") # Write label first
                    st.markdown(final_answer) # Use markdown for potentially better formatting
                except Exception as e:
                    st.error(f"An error occurred: {e}") # Display errors in the UI
        else:
            st.warning("Please enter a question.")
if __name__ == "__main__":
    home()