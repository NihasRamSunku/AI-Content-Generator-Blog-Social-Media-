import streamlit as st
from groq import Groq
import os

# ---------- SETUP ----------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Content Generator", layout="centered")
st.title("✍️ AI Content Generator (Groq Powered)")

# ---------- INPUTS ----------
topic = st.text_input("Enter Topic")

tone = st.selectbox(
    "Select Tone",
    ["Formal", "Casual", "Technical", "Creative"]
)

content_type = st.selectbox(
    "Content Type",
    ["Blog", "LinkedIn", "Twitter"]
)

word_limit = st.slider("Word Limit", 50, 1000, 300)

# ---------- FUNCTION ----------
def generate_content(topic, tone, content_type, word_limit):

    try:
        if content_type == "Blog":
            prompt = f"""
            Write ONLY a blog post about "{topic}" in a {tone} tone.
            Word limit: {word_limit}.

            Format:
            - Title
            - Introduction
            - 2–3 subheadings with content
            - Conclusion

            Do NOT include LinkedIn or Twitter formats.
            """

        elif content_type == "LinkedIn":
            prompt = f"""
            Write ONLY a LinkedIn post about "{topic}" in a {tone} tone.
            Word limit: {word_limit}.

            Format:
            - Strong hook (first line)
            - Short paragraphs
            - Add 3–5 relevant hashtags at the end

            Do NOT include blog or Twitter formats.
            """

        elif content_type == "Twitter":
            prompt = f"""
            Write ONLY a Twitter thread about "{topic}" in a {tone} tone.
            Keep total within {word_limit} words.

            Format:
            - Numbered tweets (1/, 2/, 3/...)
            - Short, punchy lines

            Do NOT include blog or LinkedIn formats.
            """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # or 70b
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# ---------- BUTTON ----------
if st.button("Generate"):
    if topic.strip() == "":
        st.warning("Please enter a topic")
    else:
        with st.spinner("Generating..."):
            result = generate_content(topic, tone, content_type, word_limit)

        st.success("Done!")
        st.write(result)