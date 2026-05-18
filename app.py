"""
SemSemty AI 🌸 — A cute pink radiology assistant made with love for Sama 💗🐾
Made with endless love by Mohamed ✨
"""
import os
from pathlib import Path
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="SemSemty AI 🌸",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. UI Persistence & Secret Message Styling
st.markdown("""
    <style>
        /* FORCE the toggle button (chevron) to stay visible when sidebar is closed */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            left: 12px !important;
            top: 12px !important;
            color: #ff4bad !important;
            background-color: white !important;
            border-radius: 50% !important;
            box-shadow: 0px 4px 12px rgba(255, 75, 173, 0.3) !important;
            z-index: 1000000 !important;
            width: 42px !important;
            height: 42px !important;
            justify-content: center !important;
            align-items: center !important;
            border: 1px solid #ffe0f0 !important;
        }

        /* Hover effect for the toggle button */
        [data-testid="collapsedControl"]:hover {
            transform: scale(1.1);
            background-color: #fff0f7 !important;
        }

        /* Subtle Branding Footer inside the sidebar */
        .sidebar-footer {
            position: fixed;
            bottom: 15px;
            left: 20px;
            font-size: 11px;
            color: #ffb6c1;
            font-family: 'Courier New', Courier, monospace;
            opacity: 0.7;
        }
        
        /* Ensure main content doesn't get hidden behind the floating button */
        .main .block-container {
            padding-top: 3rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# ── Load Environment (.env) ──────────────────────────────────────
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

# Import project-specific components
from constants.chat_data import APP_VERSION
from components.styles import inject_css
from components.sidebar import render_sidebar
from components.chat import (
    render_empty_state,
    render_chat_history,
    render_quick_actions,
    handle_chat_input,
)

# Apply baseline component styles
inject_css()

# ── Session State Initialization ─────────────────────────────────
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
# The Secret Message Tag
st.sidebar.markdown('<div class="sidebar-footer">🌸 M ❤️ S | v1.0</div>', unsafe_allow_html=True)

# Render sidebar and capture outputs
sidebar_out = render_sidebar(dict(st.session_state))

# Update state from sidebar UI
for key in ("mode", "mood", "voice_output"):
    st.session_state[key] = sidebar_out[key]

# Clear Chat functionality
if sidebar_out.get("clear"):
    for key in ["messages", "file_context", "file_name", "image_data"]:
        st.session_state[key] = defaults[key]
    st.rerun()

# Voice input handling
if sidebar_out.get("pending_voice"):
    st.session_state.pending_input = sidebar_out["pending_voice"]

# ── Main Area ────────────────────────────────────────────────────
if not st.session_state.messages:
    render_empty_state()
    render_quick_actions()
    handle_chat_input()
else:
    render_chat_history()
    handle_chat_input()
