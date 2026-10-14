import os
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="centered")

st.title("📚 AI Study Buddy")
st.caption("A beginner-friendly AI assistant for explaining concepts and creating study questions.")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

if not api_key:
    st.info("To use the AI features, add a Gemini API key as GEMINI_API_KEY in your environment or Streamlit secrets.")
    st.markdown("Get a key from Google AI Studio. Never upload your API key to GitHub.")
    st.stop()

client = genai.Client(api_key=api_key)

mode = st.selectbox(
    "Choose what you want help with",
    ["Explain a topic simply", "Create quiz questions", "Summarize notes"]
)
topic = st.text_area("Enter a topic or paste your notes", placeholder="Example: Explain Python loops with a simple example")

level = st.selectbox("Learning level", ["Beginner", "Intermediate", "Exam revision"])

if st.button("Generate", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic or some notes first.")
    else:
        instructions = {
            "Explain a topic simply": "Explain the topic in simple language, define key terms, and give one small example.",
            "Create quiz questions": "Create 5 short quiz questions about the input and provide an answer key at the end.",
            "Summarize notes": "Summarize the input as clear bullet points and list the 3 most important takeaways."
        }
        prompt = (
            "You are a friendly study assistant. "
            f"Target level: {level}. Task: {instructions[mode]}\n\n"
            f"Topic or notes:\n{topic}"
        )
        with st.spinner("Preparing your study help..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.subheader("Your study result")
                st.markdown(response.text or "No response was returned. Please try again.")
            except Exception as exc:
                st.error("The request failed. Check your API key, internet connection, and API access.")
                st.caption(f"Technical detail: {exc}")

st.divider()
st.caption("Built with Python, Streamlit, and the Gemini API. AI responses can be inaccurate; verify important information.")
