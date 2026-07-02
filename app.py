import streamlit as st
from openai import OpenAI

# --- STEP 1: INITIALIZE HUGGING FACE'S OFFICIAL CHAT API ---
HF_TOKEN = "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".strip()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

# --- STEP 2: ORANGE CAT UI THEME ---
st.set_page_config(page_title="Cindy - AI Companion", page_icon="🐾", layout="centered")

# Custom CSS for a cozy, soft ginger/orange cat aesthetic
cat_theme_css = """
<style>
    /* Cozy orange cat background color */
    .stApp {
        background-color: #F4A261;
        color: #264653;
    }
    
    /* Clean text chat styling */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    /* Style the main title */
    h1 {
        color: #1D3557 !important;
        font-weight: bold;
    }
    
    /* Subtle custom divider */
    hr {
        border-color: #E76F51 !important;
    }
</style>
"""
st.markdown(cat_theme_css, unsafe_allow_html=True)

# Main Title Header Layout
st.title("🐾 Meet Cindy")
st.caption("Your warm, highly functional NLP AI Companion")
st.markdown("---")

# Initialize conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Redraw old messages on screen smoothly
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- STEP 3: HIGHLY FUNCTIONAL CHAT PIPELINE ---
if user_input := st.chat_input("Talk to Cindy..."):
    
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Get AI Response
    with st.chat_message("assistant"):
        with st.spinner("Cindy is typing..."):
            try:
                # System prompt officially updates her persona name to Cindy
                api_messages = [{"role": "system", "content": "You are Cindy, a warm, kind, and supportive virtual friend. Always refer to yourself as Cindy."}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})

                completion = client.chat.completions.create(
                    model="meta-llama/Llama-3.1-8B-Instruct",
                    messages=api_messages,
                    max_tokens=500
                )
                
                reply = completion.choices[0].message.content
                
            except Exception as e:
                reply = f"Connection hiccup! Please try re-sending. (Error: {str(e)})"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})