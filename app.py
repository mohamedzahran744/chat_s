import os
from pathlib import Path
import streamlit as st

# 1. Basic Page Configuration
st.set_page_config(
    page_title="SemSemty AI 🌸",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. UI Persistence & Secret Message Styling
# 🌸 SemSemty AI — A cute pink radiology assistant made for Sama 💗🐾
# ✨ Made with endless love by Mohamed
st.markdown("""
    <style>
        /* Force Sidebar Visibility */
        [data-testid="stSidebar"] {
            transform: none !important;
            visibility: visible !important;
            min-width: 300px !important;
            max-width: 300px !important;
            border-right: 2px solid rgba(255, 75, 173, 0.2);
        }

        /* Keep the Open/Close Sign Always Visible */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            left: 0 !important;
            color: #ff4bad !important;
            background-color: white !important;
            border-radius: 0 50% 50% 0 !important;
            box-shadow: 2px 2px 8px rgba(255, 75, 173, 0.3) !important;
            z-index: 1000000 !important;
        }

        /* Hide the internal 'X' to discourage closing from inside */
        [data-testid="stSidebar"] button[kind="header"] {
            display: none !important;
        }

        /* Subtle Branding Footer in Sidebar */
        .sidebar-footer {
            position: fixed;
            bottom: 15px;
            left: 20px;
            font-size: 11px;
            color: #ffb6c1;
            font-family: 'Courier New', Courier, monospace;
        }
    </style>
""", unsafe_allow_html=True)

# ── Environment & Imports ────────────────────────────────────────
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

# Apply component-specific styles
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

# ── Sidebar Content ──────────────────────────────────────────────
# Secret tag in the sidebar
st.sidebar.markdown('<div class="sidebar-footer">SemSemty AI 🌸 v1.0</div>', unsafe_allow_html=True)

sidebar_out = render_sidebar(dict(st.session_state))

# Sync sidebar changes to session state
for key in ("mode", "mood", "voice_output"):
    st.session_state[key] = sidebar_out[key]

if sidebar_out.get("clear"):
    for key in ["messages", "file_context", "file_name", "image_data"]:
        st.session_state[key] = defaults[key]
    st.rerun()

if sidebar_out.get("pending_voice"):
    st.session_state.pending_input = sidebar_out["pending_voice"]

# ── Main Chat Area ───────────────────────────────────────────────
if not st.session_state.messages:
    render_empty_state()
    render_quick_actions()
    handle_chat_input()
else:
    render_chat_history()
    handle_chat_input()
