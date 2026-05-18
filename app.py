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

# 2. Strong UI Overrides & Secret Message Styling
st.markdown("""
    <style>
        /* Target BOTH potential Streamlit collapsed button containers */
        [data-testid="collapsedControl"], 
        .stSidebarCollapseButton,
        button[aria-label="Open sidebar"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            
            /* Position it prominently in the upper left corner over your background */
            position: fixed !important;
            left: 20px !important;
            top: 20px !important;
            z-index: 9999999 !important;
            
            /* High contrast design against your dark theme */
            color: #ffffff !important;
            background-color: #ff4bad !important; /* SemSemty Pink */
            border-radius: 50% !important;
            width: 45px !important;
            height: 45px !important;
            box-shadow: 0px 4px 15px rgba(255, 75, 173, 0.6) !important;
            
            /* Center the chevron icon inside the circle */
            justify-content: center !important;
            align-items: center !important;
            border: 2px solid #ffffff !important;
            transition: transform 0.2s ease, background-color 0.2s ease !important;
        }

        /* Hover animation so it feels responsive and alive */
        [data-testid="collapsedControl"]:hover,
        button[aria-label="Open sidebar"]:hover {
            transform: scale(1.15) !important;
            background-color: #ff1f93 !important;
            cursor: pointer !important;
        }

        /* Ensure the internal icon itself inherits the correct bright white color */
        [data-testid="collapsedControl"] svg,
        button[aria-label="Open sidebar"] svg {
            fill: #ffffff !important;
            color: #ffffff !important;
            width: 24px !important;
            height: 24px !important;
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
        
        /* Add safety spacing to prevent top element collisions */
        .main .block-container {
            padding-top: 4rem !important;
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
