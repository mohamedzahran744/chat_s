import os
from pathlib import Path
import streamlit as st

# 1. الإعدادات الأساسية
st.set_page_config(
    page_title="SemSemty AI 🌸",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Advanced CSS for Sidebar and Secret Message
st.markdown("""
    <style>
        /* The Secret Message (Hidden in Source/UI) */
        /* SemSemty AI 🌸 — A cute pink radiology assistant made with love for Sama 💗🐾 */
        /* Made with endless love by Mohamed ✨ */

        /* Force Sidebar to stay visible and style the toggle */
        [data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 300px !important;
        }

        /* Make sure the opening/closing chevron is always visible and pink */
        [data-testid="collapsedControl"] {
            display: flex !important;
            color: #ff4bad !important;
            background-color: rgba(255, 75, 173, 0.1);
            border-radius: 0 10px 10px 0;
        }

        /* Custom style for the secret footer in the sidebar */
        .sidebar-footer {
            position: fixed;
            bottom: 10px;
            left: 10px;
            font-size: 10px;
            color: #ffb6c1;
            opacity: 0.5;
        }
    </style>
""", unsafe_allow_html=True)

# ── Secret Message Injection (Visible only if you look closely) ──
st.sidebar.markdown('<div class="sidebar-footer">🌸 S.A.I. v1.0 - M❤️S</div>', unsafe_allow_html=True)

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

# Import custom components (Ensure these files exist in your directory)
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
sidebar_out = render_sidebar(dict(st.session_state))

# Update session state based on sidebar interactions
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
