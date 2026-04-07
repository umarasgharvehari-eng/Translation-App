import streamlit as st
from groq import Groq

# Page config
st.set_page_config(page_title="AI Translator", page_icon="🌍", layout="wide")


# Initialize Groq client using Streamlit secrets
def get_client():
    if "Translation" not in st.secrets:
        st.error("Missing secret: 'Translation'. Add your Groq API key in Streamlit secrets.")
        st.stop()

    api_key = st.secrets["Translation"]

    if not api_key or not str(api_key).strip():
        st.error("API key is empty. Please check your Streamlit secrets.")
        st.stop()

    return Groq(api_key=api_key)


# Supported languages
SUPPORTED_LANGUAGES = [
    "English",
    "Urdu",
    "Arabic",
    "Hindi",
    "French",
    "Spanish",
    "German",
    "Chinese",
    "Japanese",
]

MODEL = "llama-3.3-70b-versatile"


# Translation function
def translate_text(text, source_language, target_language):
    client = get_client()

    prompt = f"""
Translate the following text from {source_language} to {target_language}.

Rules:
- Return only translated text
- No explanation
- Preserve meaning and tone
- Keep formatting if possible

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()


# UI
st.title("🌍 Multilingual Translator")
st.caption("Powered by Groq + Streamlit")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    source_language = st.selectbox("Source Language", SUPPORTED_LANGUAGES, index=0)
    input_text = st.text_area("Enter text to translate", height=250)

with col2:
    st.subheader("Output")
    target_language = st.selectbox("Target Language", SUPPORTED_LANGUAGES, index=1)
    output_box = st.empty()


# Translate button
if st.button("Translate", type="primary", use_container_width=True):
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    elif source_language == target_language:
        st.warning("Source and target languages must be different.")
    else:
        try:
            with st.spinner("Translating..."):
                result = translate_text(input_text, source_language, target_language)

            output_box.success(result)

        except Exception as e:
            st.error(f"Translation failed: {e}")
