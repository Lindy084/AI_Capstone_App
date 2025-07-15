import streamlit as st
from accessibility_tool import accessibility_ui
from custom_tool import (
    cv_keyword_checker_ui,
    pdf_summarizer_ui,
    image_captioning_ui
)
from study_buddy import study_buddy_ui
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Sidebar Navigation ---
st.sidebar.title("🛠️ Select Tool")
menu = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "Study Buddy",
    "Accessibility Tool",
    "Custom Tool"
])

# --- Homepage ---
if menu == "🏠 Home":
    st.title("💡 Lindiwe Ndlazi – AI Capstone Project")
    st.markdown("---")
    st.image("https://cdn-icons-png.flaticon.com/512/4703/4703702.png", width=100)
    st.markdown("""
    ### 🌟 Welcome to My AI Capstone Tools!
    This project showcases practical, real-world applications of AI that enhance **accessibility**, **career readiness**, and **learning support**.

    **Key Tools Included:**
    - 🧠 **Study Buddy** – Chat with your learning companion  
    - 🗣️ **Accessibility Tool** – Voice ↔ Text  
    - 📄 **CV Keyword Checker** – Match your CV with job descriptions  
    - 📚 **PDF Summarizer** – Quickly summarize long documents  
    - 🖼️ **Image Captioning** – Get AI-generated captions for images  

    ---
    #### 📚 About Me
    I'm **Lindiwe Ndlazi**, a passionate AI learner and developer based in Johannesburg 🇿🇦.
    This Capstone is a reflection of my journey — combining human potential and intelligent tools to create impact.

    🔗 [My LinkedIn](https://www.linkedin.com/in/ndlazi-lindiwe-76baa6229)
    ---
    """)
    st.info("👈 Use the sidebar to explore each tool")

elif menu == "Study Buddy":
    study_buddy_ui()

elif menu == "Accessibility Tool":
    accessibility_ui()

elif menu == "Custom Tool":
    st.subheader("Choose a Custom Tool Feature")
    feature = st.radio("Select feature:", [
        "CV Keyword Checker",
        "PDF Summarizer",
        "Image Captioning"
    ])
    if feature == "CV Keyword Checker":
        cv_keyword_checker_ui()
    elif feature == "PDF Summarizer":
        pdf_summarizer_ui()
    elif feature == "Image Captioning":
        image_captioning_ui()
