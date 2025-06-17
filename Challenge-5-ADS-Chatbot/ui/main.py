import streamlit as st
import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from app.backend import generate_bot_response
from app.filters import is_prompt_safe_llm

st.set_page_config(page_title="Alaska Snow Department Assistant", layout="centered")
st.title("Alaska Snow Department")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Display chat history with auto-scroll effect
chat_placeholder = st.container()
with chat_placeholder:
    for msg in st.session_state.messages:
        role = "Bot" if msg["role"] == "assistant" else "User"
        st.markdown(f"**{role}**: {msg['content']}")

# Clear input before rendering widget if flag is set
if st.session_state.clear_input:
    st.session_state.user_input = ""
    st.session_state.clear_input = False

# Input field
user_input = st.text_input("Type your message:", key="user_input")

# On Send button click
if st.button("Send") and user_input.strip():
    if not is_prompt_safe_llm(user_input):
        st.error("This question blocked by the admin. Try something else.")
    else:
        try:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Generate bot response
            with st.spinner("Bot: Generating response..."):
                response = generate_bot_response(user_input)

            # Add bot response
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Set flag to clear input field
            st.session_state.clear_input = True
            st.experimental_rerun()

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
