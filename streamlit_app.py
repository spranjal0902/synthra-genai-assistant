import os
import html
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# -----------------------------
# Load API key
# -----------------------------
load_dotenv()

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=groq_api_key
)

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Synthra",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Helper function
# -----------------------------
def format_message(content):
    safe_content = html.escape(content)
    return safe_content.replace("\n", "<br>")


# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #0f172a 0%, #020617 45%, #020617 100%);
    color: #F8FAFC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 10rem;
    max-width: 1450px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #07111f 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.20);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #E5E7EB !important;
}

.sidebar-logo {
    font-size: 2rem;
    font-weight: 900;
    color: #FFFFFF;
    margin-bottom: 0.3rem;
}

.sidebar-logo span {
    background: linear-gradient(135deg, #60A5FA, #8B5CF6, #22D3EE);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sidebar-subtitle {
    color: #CBD5E1;
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 1.4rem;
}

.sidebar-card {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.20);
    padding: 1rem;
    border-radius: 16px;
    color: #CBD5E1;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(148, 163, 184, 0.25);
    background: rgba(15, 23, 42, 0.90);
    color: #F8FAFC;
    padding: 0.75rem 1rem;
    transition: all 0.25s ease;
    font-weight: 500;
}

.stButton > button:hover {
    background: rgba(37, 99, 235, 0.20);
    border-color: rgba(96, 165, 250, 0.75);
    color: white;
    transform: translateY(-1px);
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: rgba(15, 23, 42, 0.92);
    border-radius: 14px;
    border: 1px solid rgba(148, 163, 184, 0.28);
}

/* Strong slider color override */
div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background: linear-gradient(90deg, #38BDF8, #6366F1) !important;
}

div[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background-color: #6366F1 !important;
    border-color: #6366F1 !important;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.8) !important;
}

div[data-testid="stSlider"] [data-baseweb="slider"] div {
    color: #6366F1 !important;
}

/* Top badge */
.model-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    float: right;
    padding: 0.55rem 0.95rem;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.86);
    border: 1px solid rgba(148, 163, 184, 0.28);
    color: #E5E7EB;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.green-dot {
    height: 10px;
    width: 10px;
    background-color: #10B981;
    border-radius: 50%;
    display: inline-block;
}

/* Hero section */
.hero {
    position: relative;
    padding: 3rem 3.2rem;
    border-radius: 28px;
    background:
        radial-gradient(circle at 82% 42%, rgba(34, 211, 238, 0.25), transparent 22%),
        radial-gradient(circle at 18% 18%, rgba(124, 58, 237, 0.42), transparent 30%),
        linear-gradient(135deg, #24145f 0%, #0f1f57 45%, #063a55 100%);
    border: 1px solid rgba(96, 165, 250, 0.32);
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.45);
    margin-bottom: 1.5rem;
    overflow: hidden;
    min-height: 280px;
}

.hero h1 {
    font-size: 4.2rem;
    line-height: 1;
    margin-bottom: 0.8rem;
    color: #FFFFFF;
    letter-spacing: -2px;
}

.hero .tagline {
    font-size: 1.35rem;
    font-weight: 800;
    background: linear-gradient(90deg, #22D3EE, #818CF8, #C084FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero .desc {
    margin-top: 1.4rem;
    font-size: 1.05rem;
    color: #CBD5E1;
    max-width: 620px;
}

/* Hero visual */
.hero-visual {
    position: absolute;
    right: 70px;
    top: 55px;
    width: 270px;
    height: 190px;
}

.chat-card-back {
    position: absolute;
    right: 8px;
    top: 0;
    width: 155px;
    height: 112px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.30), rgba(34, 211, 238, 0.12));
    border: 1px solid rgba(125, 211, 252, 0.45);
    box-shadow: 0 0 38px rgba(37, 99, 235, 0.38);
}

.chat-card-mid {
    position: absolute;
    right: 45px;
    top: 38px;
    width: 155px;
    height: 108px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.38), rgba(14, 165, 233, 0.18));
    border: 1px solid rgba(147, 197, 253, 0.48);
    box-shadow: 0 0 38px rgba(99, 102, 241, 0.32);
}

.chat-bubble-front {
    position: absolute;
    right: 105px;
    top: 76px;
    width: 124px;
    height: 78px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.60), rgba(14, 165, 233, 0.40));
    border: 1px solid rgba(125, 211, 252, 0.58);
    box-shadow: 0 0 38px rgba(34, 211, 238, 0.38);
}

.chat-bubble-front::after {
    content: "";
    position: absolute;
    left: 22px;
    bottom: -13px;
    border-width: 14px 14px 0 0;
    border-style: solid;
    border-color: rgba(14, 165, 233, 0.42) transparent transparent transparent;
}

.dot {
    position: absolute;
    top: 33px;
    width: 12px;
    height: 12px;
    background: #22D3EE;
    border-radius: 999px;
    box-shadow: 0 0 16px rgba(34, 211, 238, 0.95);
}

.dot1 {
    left: 32px;
}

.dot2 {
    left: 56px;
}

.dot3 {
    left: 80px;
}

.orbit {
    position: absolute;
    right: 50px;
    bottom: 4px;
    width: 200px;
    height: 50px;
    border-radius: 50%;
    border: 1px solid rgba(99, 102, 241, 0.58);
    transform: rotate(-8deg);
    box-shadow: 0 0 38px rgba(37, 99, 235, 0.38);
}

/* Feature cards */
.feature-card {
    padding: 1.6rem;
    border-radius: 22px;
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.62));
    border: 1px solid rgba(148, 163, 184, 0.24);
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.28);
    min-height: 170px;
    transition: all 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-3px);
    border-color: rgba(96, 165, 250, 0.55);
    box-shadow: 0 25px 65px rgba(37, 99, 235, 0.16);
}

.icon-box {
    width: 46px;
    height: 46px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    margin-bottom: 1rem;
}

.blue-icon {
    background: rgba(37, 99, 235, 0.24);
    border: 1px solid rgba(96, 165, 250, 0.48);
}

.cyan-icon {
    background: rgba(6, 182, 212, 0.20);
    border: 1px solid rgba(34, 211, 238, 0.45);
}

.purple-icon {
    background: rgba(124, 58, 237, 0.24);
    border: 1px solid rgba(168, 85, 247, 0.48);
}

.feature-card h3 {
    color: #F8FAFC;
    margin-bottom: 0.5rem;
    font-size: 1.35rem;
}

.feature-card p {
    color: #CBD5E1;
    line-height: 1.6;
}

/* Chat title */
.chat-title {
    margin-top: 2rem;
    margin-bottom: 2rem;
    font-size: 1.9rem;
    font-weight: 850;
    color: #F8FAFC;
}

/* Custom chat layout - spacious version */
.user-message {
    width: min(78%, 980px);
    margin-left: auto;
    margin-right: 0;
    margin-top: 1.4rem;
    margin-bottom: 2.2rem;
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.34), rgba(99, 102, 241, 0.24));
    border: 1px solid rgba(96, 165, 250, 0.55);
    border-radius: 24px 24px 8px 24px;
    padding: 1.35rem 1.65rem;
    color: #F8FAFC;
    box-shadow: 0 16px 40px rgba(37, 99, 235, 0.15);
}

.assistant-message {
    width: min(88%, 1120px);
    margin-left: 0;
    margin-right: auto;
    margin-top: 0.6rem;
    margin-bottom: 3.5rem;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(8, 47, 73, 0.74));
    border: 1px solid rgba(34, 211, 238, 0.32);
    border-radius: 24px 24px 24px 8px;
    padding: 1.7rem 2rem;
    color: #E5E7EB;
    box-shadow: 0 18px 48px rgba(6, 182, 212, 0.13);
}

.message-label {
    font-size: 0.78rem;
    font-weight: 850;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.95rem;
    opacity: 0.92;
}

.user-label {
    color: #93C5FD;
}

.assistant-label {
    color: #22D3EE;
}

.message-content {
    font-size: 1.06rem;
    line-height: 1.9;
    color: #F8FAFC;
    word-wrap: break-word;
}

/* Chat input */
div[data-testid="stChatInput"] {
    background: rgba(15, 23, 42, 0.90);
    border-radius: 18px;
}

/* Give extra space above fixed chat input */
section.main > div {
    padding-bottom: 8rem;
}

/* Footer */
.footer {
    text-align: center;
    color: #94A3B8;
    margin-top: 2rem;
    margin-bottom: 5rem;
    font-size: 0.9rem;
}

/* Mobile */
@media (max-width: 900px) {
    .hero-visual {
        display: none;
    }

    .hero h1 {
        font-size: 3rem;
    }

    .hero {
        padding: 2rem;
    }

    .user-message,
    .assistant-message {
        width: 95%;
        max-width: 95%;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown("""
<div class="sidebar-logo"><span>✦</span> Synthra</div>
<div class="sidebar-subtitle">Smart conversations.<br>Real growth.</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

assistant_mode = st.sidebar.selectbox(
    "ASSISTANT MODE",
    [
        "AI Tutor",
        "Career Mentor",
        "Email Rewriter",
        "Text Summarizer",
        "Interview Coach"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### SETTINGS")

temperature = st.sidebar.slider(
    "Creativity (Temperature)",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)

max_tokens = st.sidebar.slider(
    "Response Length (Max Tokens)",
    min_value=200,
    max_value=1200,
    value=700,
    step=100
)

mode_prompts = {
    "AI Tutor": "Explain AI and LLM concepts in simple beginner-friendly language with examples.",
    "Career Mentor": "Guide students and early-career professionals toward AI, GenAI, and LLM roles.",
    "Email Rewriter": "Rewrite informal text into clear, polite, and professional communication.",
    "Text Summarizer": "Summarize long text into clear, structured, easy-to-read points.",
    "Interview Coach": "Prepare users for AI, GenAI, and LLM interviews with practical answers."
}

final_system_prompt = SYSTEM_PROMPT + "\n\nCurrent assistant mode: " + mode_prompts[assistant_mode]

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": final_system_prompt}
    ]
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### QUICK START")

example_prompts = {
    "Explain hallucination": "Explain LLM hallucination in simple words with one example.",
    "Rewrite email": "Rewrite this professionally: hey, I wanted to ask if there is any update about my application.",
    "Interview prep": "Ask me 5 beginner interview questions for a GenAI internship.",
    "Learning roadmap": "Create a 4-week roadmap to become ready for GenAI internships."
}

selected_prompt = None

for label, prompt in example_prompts.items():
    if st.sidebar.button(label):
        selected_prompt = prompt

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-card">
<b>ABOUT SYNTHRA</b><br><br>
Synthra is a prompt-engineered GenAI assistant built with Python, Streamlit, Groq API, LLaMA, and session-state memory.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Main UI
# -----------------------------
st.markdown("""
<div class="model-badge">
<span class="green-dot"></span>
Powered by Groq · LLaMA 3.3 70B
</div>
""", unsafe_allow_html=True)

hero_html = """
<div style="clear: both;"></div>
<div class="hero">
<h1>Synthra</h1>
<div class="tagline">Smart conversations. Real growth.</div>
<div class="desc">Your AI companion for learning, career growth, and productivity.</div>
<div class="hero-visual">
<div class="orbit"></div>
<div class="chat-card-back"></div>
<div class="chat-card-mid"></div>
<div class="chat-bubble-front">
<div class="dot dot1"></div>
<div class="dot dot2"></div>
<div class="dot dot3"></div>
</div>
</div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div class="feature-card">
<div class="icon-box blue-icon">🎓</div>
<h3>Learn</h3>
<p>Understand AI, GenAI, and LLM concepts in simple language.</p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="feature-card">
<div class="icon-box cyan-icon">💼</div>
<h3>Grow</h3>
<p>Get career guidance, project ideas, and interview preparation support.</p>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div class="feature-card">
<div class="icon-box purple-icon">✍️</div>
<h3>Create</h3>
<p>Rewrite emails, summarize text, and improve professional communication.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-title">Chat with Synthra</div>', unsafe_allow_html=True)

# -----------------------------
# Chat state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": final_system_prompt}
    ]

st.session_state.messages[0] = {
    "role": "system",
    "content": final_system_prompt
}

# -----------------------------
# Display existing messages
# -----------------------------
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f"""
<div class="user-message">
<div class="message-label user-label">You</div>
<div class="message-content">{format_message(message["content"])}</div>
</div>
""",
            unsafe_allow_html=True
        )

    elif message["role"] == "assistant":
        st.markdown(
            f"""
<div class="assistant-message">
<div class="message-label assistant-label">Synthra</div>
<div class="message-content">{format_message(message["content"])}</div>
</div>
""",
            unsafe_allow_html=True
        )

# -----------------------------
# User input
# -----------------------------
user_input = st.chat_input("Ask Synthra anything...")

if selected_prompt:
    user_input = selected_prompt

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    st.markdown(
        f"""
<div class="user-message">
<div class="message-label user-label">You</div>
<div class="message-content">{format_message(user_input)}</div>
</div>
""",
        unsafe_allow_html=True
    )

    with st.spinner("Synthra is thinking..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            assistant_reply = response.choices[0].message.content

            st.markdown(
                f"""
<div class="assistant-message">
<div class="message-label assistant-label">Synthra</div>
<div class="message-content">{format_message(assistant_reply)}</div>
</div>
""",
                unsafe_allow_html=True
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_reply}
            )

        except Exception as e:
            st.error("Something went wrong. Please check your Groq API key, internet connection, or model access.")
            st.code(str(e))

# -----------------------------
# Download chat
# -----------------------------
chat_text = ""

for message in st.session_state.messages:
    if message["role"] != "system":
        chat_text += f"{message['role'].upper()}: {message['content']}\n\n"

st.sidebar.download_button(
    label="Download Chat",
    data=chat_text,
    file_name="synthra_chat_history.txt",
    mime="text/plain"
)

st.markdown("""
<div class="footer">
Built with Python · Streamlit · Groq · LLaMA
</div>
""", unsafe_allow_html=True)