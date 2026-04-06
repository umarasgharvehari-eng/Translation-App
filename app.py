import streamlit as st
from groq import Groq

st.set_page_config(page_title="Translator", page_icon="🌍")

# Get API key from Streamlit secrets
api_key = st.secrets["Translation"]

client = Groq(api_key=api_key)

SUPPORTED_LANGUAGES = [
    "English",
    "Urdu",
    "Arabic",
    "Hindi",
    "French",
    "Spanish",
    "German"
]

MODEL = "llama-3.3-70b-versatile"


def translate(text, source, target):
    prompt = f"""
Translate the following text from {source} to {target}.

Rules:
- Only return translated text
- No explanation

Text:
{text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


# UI
st.title("🌍 English ↔ Urdu Translator")
st.write("Powered by Groq + Streamlit")

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Source", SUPPORTED_LANGUAGES)
    input_text = st.text_area("Enter text")

with col2:
    target_lang = st.selectbox("Target", SUPPORTED_LANGUAGES, index=1)
    output_text = st.empty()

if st.button("Translate"):
    if input_text.strip() == "":
        st.warning("Enter text first")
    else:
        with st.spinner("Translating..."):
            result = translate(input_text, source_lang, target_lang)
            output_text.success(result)
