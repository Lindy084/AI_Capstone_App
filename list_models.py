import streamlit as st
import requests

# 🔐 Load OpenRouter API key from Streamlit secrets
api_key = st.secrets.get("OPENROUTER_API_KEY")

if not api_key:
    st.warning("⚠️ OPENROUTER_API_KEY not found. Add it to .streamlit/secrets.toml or Streamlit Cloud Secrets.")
else:
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
        models = response.json().get('data', [])

        st.subheader("🔍 Available OpenRouter Models:")
        for m in models:
            model_id = m.get('id')
            is_free = m.get('pricing', {}).get('prompt') == "0.0000000"
            st.markdown(f"- `{model_id}` {'(free)' if is_free else ''}")
    except Exception as e:
        st.error(f"❌ Failed to fetch models: {e}")
