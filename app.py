"""
SemSemty AI 🌸 — A cute pink radiology assistant made with love for Sama 💗🐾
Made with endless love by Mohamed ✨
"""
import os
from pathlib import Path
import streamlit as st

# 1. Page Config
st.set_page_config(
    page_title="SemSemty AI 🌸",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. CSS to allow opening/closing while keeping the toggle visible
st.markdown("""
    <style>
        /* Ensure the 'Open/Close' toggle sign (chevron) is ALWAYS visible */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            color: #ff4bad !important; /* SemSemty Pink */
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 0 10px 10px 0 !important;
            left: 0 !important;
            z-index: 1000000 !important;
            box-shadow: 2px 2px 10px rgba(255, 75, 173, 0.2) !important;
        }

        /* Hover effect for the toggle sign */
        [data-testid="collapsedControl"]:hover {
            color: #ff1f93 !important;
            background-color: #fff0f7 !important;
        }

        /* Subtle Branding Footer for the sidebar */
        .sidebar-secret-footer {
            position: fixed;
            bottom: 10px;
            left: 10px;
            font-size: 10px;
            color: #ffb6c1;
            opacity: 0.6;
            z-index: 99;
        }
    </style>
""", unsafe_allow_html=True)

# ── Load .env ────────────────────────────────────────────────────
_env_path = Path(__file__).parent / ".env"
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=_env_path, override=True)
except ImportError:
    if _env_path.exists():
        for line in _env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from constants.chat_data import APP_VERSION
from components.styles import inject_css
from components.sidebar import render_sidebar
from components.chat import (
    render_empty_state,
    render_chat_history,
    render_quick_actions,
    handle_chat_input,
)

inject_css()

# ── Session state defaults ───────────────────────────────────────
defaults = {
    "messages":          [],
    "mode":              "🩻 Radiology Q&A",
    "mood":              "😊 Happy",
    "file_context":      "",
    "file_name":         "",
    "total_messages":    0,
    "total_files":       0,
    "pending_input":     None,
    "voice_output":      False,
    "image_data":        None,
    "image_media_type":  "image/jpeg",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ──────────────────────────────────────────────────────
# Secret Message in Sidebar UI (Stays hidden/subtle at bottom)
st.sidebar.markdown('<div class="sidebar-secret-footer">🌸 M ❤️ S</div>', unsafe_allow_html=True)

sidebar_out = render_sidebar(dict(st.session_state))

# Update logic
for key in ("mode", "mood", "voice_output"):
    st.session_state[key] = sidebar_out[key]

if sidebar_out.get("clear"):
    st.session_state.messages = []
    st.session_state.file_context = ""
    st.session_state.file_name = ""
    st.session_state.image_data = None
    st.session_state.image_media_type = "image/jpeg"
    st.rerun()

if sidebar_out.get("pending_voice"):
    st.session_state.pending_input = sidebar_out["pending_voice"]

# ── Main area ────────────────────────────────────────────────────
if not st.session_state.messages:
    render_empty_state()
    render_quick_actions()
    handle_chat_input()
else:
    render_chat_history()
    handle_chat_input()
