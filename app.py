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

# 2. CSS to lock sidebar and keep toggle visible
st.markdown("""
    <style>
        /* Force sidebar to stay visible and prevent sliding away */
        [data-testid="stSidebar"] {
            transform: none !important;
            visibility: visible !important;
            min-width: 300px !important;
        }

        /* Ensure the 'Open/Close' toggle sign is always visible and pink */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            color: #ff4bad !important;
            background-color: rgba(255, 255, 255, 0.8) !important;
            border-radius: 0 10px 10px 0 !important;
            left: 0 !important;
            z-index: 1000000 !important;
        }

        /* Hide the 'X' close button inside the sidebar to prevent accidental closing */
        [data-testid="stSidebar"] button[kind="header"] {
            display: none !important;
        }

        /* Secret branding footer for the sidebar */
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
# Secret Message in Sidebar UI
st.sidebar.markdown('<div class="sidebar-secret-footer">🌸 M ❤️ S</div>', unsafe_allow_html=True)

sidebar_out = render_sidebar(dict(st.session_state))
for key in ("mode", "mood", "voice_output"):
    st.session_state[key] = sidebar_out[key]

if sidebar_out.get("clear"):
    st.session_state.messages         = []
    st.session_state.file_context      = ""
    st.session_state.file_name         = ""
    st.session_state.image_data        = None
    st.session_state.image_media_type  = "image/jpeg"
    st.rerun()

if sidebar_out.get("pending_voice"):
    st.session_state.pending_input = sidebar_out["pending_voice"]

# ── Main area ────────────────────────────────────────────────────
has_messages = bool(st.session_state.messages)

if not has_messages:
    render_empty_state()
    render_quick_actions()
    handle_chat_input()
else:
    render_chat_history()
    handle_chat_input()
