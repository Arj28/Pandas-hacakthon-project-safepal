import streamlit as st
from transformers import pipeline
import random
import requests
import streamlit.components.v1 as components

# Page Config
st.set_page_config(page_title="SafePal: Your Safety Companion", layout="centered")
st.title("🛡️ SafePal - Your AI Safety Companion")

# Tabs for features
tab1, tab2, tab3 = st.tabs(["🧠 SafeChat", "📍 Emergency Tools", "🔬 About"])

# Load pipelines
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)
generator = pipeline("text-generation", model="gpt2")

# Whisper code
WHISPER_CODE = "call me now"

# Store chat session
if "chat" not in st.session_state:
    st.session_state.chat = []

# Helper: Fake call name
def generate_fake_call_name():
    callers = ["Mom", "Boss", "Friend", "Neighbor"]
    return f"📞 Incoming call from {random.choice(callers)}... (This is a fake emergency call)"

# Helper: Fake call script
def generate_fake_call(topic="going to the market"):
    prompt = f"A fake phone call conversation between two friends talking about {topic}:"
    result = generator(prompt, max_length=100, num_return_sequences=1)
    return result[0]['generated_text']

# Helper: IP-based location
def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return f"{data['city']}, {data['region']}, {data['country']}"
    except:
        return "Location not available"

# ------------------- Tab 1: SafeChat -------------------
with tab1:
    st.subheader("🧠 Talk to SafePal")

    st.selectbox("Choose Language", ["English", "Urdu", "Spanish", "Arabic"], index=0)

    

    # Text fallback
    user_input = st.text_input("Or type your message...")

    if user_input:
        st.session_state.chat.append(("🧍‍♀️ You", user_input))

        if WHISPER_CODE in user_input.lower():
            st.warning("🚨 Emergency whisper code detected!")
            st.session_state.chat.append(("📞 SafePal", generate_fake_call_name()))
        else:
            sentiment = sentiment_analyzer(user_input)[0]
            if sentiment["label"] == "NEGATIVE":
                st.session_state.chat.append(("📞 SafePal", "I'm here for you. Stay calm. Do you need help?"))
            else:
                st.session_state.chat.append(("📞 SafePal", "Thank you for sharing. I'm with you."))

    for sender, msg in st.session_state.chat:
        st.markdown(f"**{sender}:** {msg}")

    st.markdown("---")

# ------------------- Tab 2: Emergency Tools -------------------
with tab2:
    st.subheader("📍 Emergency Tools")

    if st.button("📡 Show My Location"):
        st.info(f"📍 Your Location: {get_location()}")

    if st.button("🚨 Panic Button"):
        st.error("🚨 Alert Sent! Stay Safe.")

    if st.button("📞 Trigger Fake Call"):
        st.info(generate_fake_call_name())

    st.caption("🗣️ You can also whisper or type **'call me now'** to trigger fake call silently.")

    st.markdown("---")

    st.write("🎭 Want a fake call conversation to distract?")
    topic = st.text_input("Topic for fake call", value="going to the market")
    if st.button("Generate Fake Call Script"):
        fake_call_script = generate_fake_call(topic)
        st.text_area("🎤 Fake Call Script", fake_call_script, height=200)

    st.markdown("---")

# ------------------- Tab 3: About -------------------
with tab3:
    st.subheader("🔬 About SafePal")
    st.markdown("""
    **SafePal** is your AI-powered companion designed to assist you in unsafe or uncomfortable situations.

    **Features:**
    - 💬 Chat and emotional support via sentiment analysis
    - 🧠 Detect distress through negative sentiment
    - 🗣️ Trigger fake call via **whisper code**
    - 📍 Share your approximate live location
    - 🚨 Panic alert for emergencies
    - 🎭 Generate fake call conversation scripts for distraction

    **Built with:** Streamlit + Hugging Face Transformers
    """)
