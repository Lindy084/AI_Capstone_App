import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
from PIL import Image
import openai  # Needed if you use OpenAI APIs
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key  # Assign to OpenAI client

if not api_key:
    st.warning("⚠️ OPENAI_API_KEY not found. Please set it in your .env file.")

# ---------------- CV Keyword Checker ---------------- #
def cv_keyword_checker_ui():
    st.header("🔍 CV Keyword Checker")
    uploaded_file = st.file_uploader("Upload your CV (PDF or TXT)", type=["pdf", "txt"])

    keywords_input = st.text_input("Enter job description keywords (comma separated)")
    match_type = st.radio("Choose keyword match type:", ["Whole word match", "Substring match"])

    if uploaded_file and keywords_input:
        keywords = [kw.strip().lower() for kw in keywords_input.split(",") if kw.strip()]
        file_text = ""

        if uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                file_text += page.extract_text() or ""
        else:
            file_text = uploaded_file.read().decode("utf-8")

        preview_text = file_text[:1500] + "..." if len(file_text) > 1500 else file_text
        st.subheader("📄 Your CV Text Preview")
        st.write(preview_text)

        text_lower = file_text.lower()
        matched = []
        for kw in keywords:
            if match_type == "Whole word match":
                if f" {kw} " in text_lower:
                    matched.append(kw)
            else:
                if kw in text_lower:
                    matched.append(kw)

        match_score = round(len(matched) / len(keywords) * 100, 2) if keywords else 0

        st.success(f"✅ Matched Keywords:\n{', '.join(matched) if matched else 'No matches'}")
        st.metric("📊 Match Score", f"{match_score}%")

        # Highlight keywords
        st.subheader("📄 CV Preview with highlighted keywords:")
        highlighted_text = file_text
        for kw in matched:
            highlighted_text = highlighted_text.replace(kw, f"**{kw.upper()}**")

        st.markdown(highlighted_text[:1500] + "...", unsafe_allow_html=True)


# ---------------- PDF Summarizer ---------------- #
def pdf_summarizer_ui():
    st.header("📄 PDF Summarizer")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() or ""

        if not full_text.strip():
            st.warning("⚠️ No text found in the PDF.")
            return

        st.subheader("📖 Extracted Text")
        st.text_area("Raw Text", full_text, height=200)

        # Dummy summary logic
        summary = full_text[:300] + "..." if len(full_text) > 300 else full_text

        st.subheader("📝 Summary")
        st.write(summary)

        # ✅ Download Button
        summary_bytes = BytesIO(summary.encode("utf-8"))
        st.download_button(
            label="📥 Download Summary",
            data=summary_bytes,
            file_name="pdf_summary.txt",
            mime="text/plain"
        )


# ---------------- Image Captioning ---------------- #
def image_captioning_ui():
    st.header("🖼️ Image Captioning")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Dummy caption
        caption = "This is a placeholder caption for your image."

        st.subheader("📝 Caption")
        st.write(caption)

        # ✅ Download Button
        caption_bytes = BytesIO(caption.encode("utf-8"))
        st.download_button(
            label="📥 Download Caption",
            data=caption_bytes,
            file_name="image_caption.txt",
            mime="text/plain"
        )
