import streamlit as st
import json
from gtts import gTTS
import base64
from io import BytesIO
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    # Case-insensitive match
    matched = None
    for q in answers:
        if q.strip().lower() == question.strip().lower():
            matched = q
            break

    if matched:
        response = answers[matched]
    else:
        # Use OpenAI if not matched
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        response = completion.choices[0].message["content"].strip()

    # Show and speak response
    st.write("🤖 " + response)
    speak(response)
