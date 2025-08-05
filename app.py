import streamlit as st
import json
from gtts import gTTS
import base64
from io import BytesIO
from openai import OpenAI

# Initialize OpenAI client (replace below with your API key if needed)
client = OpenAI(api_key="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")  # 👈 Replace with your actual key

# Load predefined answers
with open("responses.json", "r") as f:
    answers = json.load(f)

# Title
st.title("🎙️ My Voice Bot - AI Interview Demo")
st.write("Ask me a question!")

# Input box
question = st.text_input("Enter a question you'd like to ask me:")

# Function to speak the response
def speak(text):
    tts = gTTS(text)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio_data = mp3_fp.read()
    b64 = base64.b64encode(audio_data).decode()
    audio_html = f"""
        <audio autoplay controls>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(audio_html, unsafe_allow_html=True)

# When question is asked
if question:
    if question in answers:
        response = answers[question]
    else:
        # Fallback to ChatGPT with latest OpenAI client
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        response = chat_completion.choices[0].message.content

    st.write("🤖 " + response)
    speak(response)
