import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def ask_ai(question):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-3.5-turbo-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that answers clearly."},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    try:
        full_json = response.json()
        st.code(full_json)  # Optional: show raw response for debugging
        return full_json['choices'][0]['message']['content']
    except Exception as e:
        st.error("🔍 Something went wrong:")
        st.code(response.text)
        return f"❌ Error: {str(e)}"

def study_buddy_ui():
    st.header("💬 Study Buddy – Ask Me Anything!")
    st.write("Ask about any topic – AI, maths, careers, or daily life.")
    user_input = st.text_input("Type your question:")

    if user_input:
        with st.spinner("Thinking... 🤔"):
            reply = ask_ai(user_input)
            st.success("🤖 " + reply)
