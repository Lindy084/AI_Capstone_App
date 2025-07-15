import os
from dotenv import load_dotenv
import streamlit as st
from gtts import gTTS
import tempfile
import speech_recognition as sr
from io import BytesIO

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.warning("⚠️ OPENAI_API_KEY not found. Set it in a .env file.")

def accessibility_ui():
    st.header("🗣️ Accessibility Tool – Voice ↔ Text")

    # --- Text to Speech ---
    st.subheader("🔊 Text to Speech")
    text_input = st.text_area("Enter text to convert to speech:")
    if st.button("▶️ Speak It"):
        if text_input.strip() == "":
            st.warning("Please enter some text first.")
        else:
            try:
                tts = gTTS(text_input)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name, format="audio/mp3")
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

    st.markdown("---")

    # --- Voice to Text ---
    st.subheader("🎤 Voice to Text – Upload & Transcribe")
    uploaded_audio = st.file_uploader("Upload a voice recording (.wav or .mp3)", type=["wav", "mp3"])

    language_code = st.selectbox(
        "Select language for transcription",
        options=[
            ("en-US", "English (US)"),
            ("en-GB", "English (UK)"),
            ("zu", "Zulu"),
            ("af", "Afrikaans"),
            ("fr-FR", "French"),
            ("es-ES", "Spanish")
        ],
        format_func=lambda x: x[1]
    )[0]

    if uploaded_audio:
        try:
            recognizer = sr.Recognizer()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(uploaded_audio.read())
                audio_path = f.name

            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language=language_code)
                st.success("✅ Transcription successful!")
                st.session_state.transcribed_text = text
        except Exception as e:
            st.error(f"❌ Could not transcribe audio: {e}")

    st.markdown("**📝 Transcribed Text:**")
    transcript = st.session_state.get("transcribed_text", "⏳ Waiting for transcription...")
    st.code(transcript)

    if transcript and transcript != "⏳ Waiting for transcription...":
        st.download_button(
            label="📥 Download Transcript",
            data=BytesIO(transcript.encode("utf-8")),
            file_name="transcript.txt",
            mime="text/plain"
        )
