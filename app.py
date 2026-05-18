"""
SemSemty AI 🌸 — A cute pink radiology assistant made with love for Sama 💗🐾
Made with endless love by Mohamed ✨
"""
# ── Load .env with absolute path — works everywhere ──────────────
import os
from pathlib import Path

_env_path = Path(__file__).parent / ".env"
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=_env_path, override=True)
except ImportError:
    # Fallback: manually parse .env
    if _env_path.exists():
        for line in _env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

import streamlit as st

st.set_page_config(
    page_title="SemSemty AI 🌸",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
for key in ("mode", "mood", "voice_output"):
    st.session_state[key] = sidebar_out[key]

if sidebar_out.get("clear"):
    st.session_state.messages         = []
    st.session_state.file_context     = ""
    st.session_state.file_name        = ""
    st.session_state.image_data       = None
    st.session_state.image_media_type = "image/jpeg"
    st.rerun()

if sidebar_out.get("pending_voice"):
    st.session_state.pending_input = sidebar_out["pending_voice"]

# ── Main area ────────────────────────────────────────────────────
has_messages = bool(st.session_state.messages)

if not has_messages:
    # Empty state & quick actions rendered OUTSIDE any chat context
    render_empty_state()
    render_quick_actions()
    handle_chat_input()
else:
    render_chat_history()
    handle_chat_input()
