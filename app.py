"""
SemSemty AI 🌸 — A cute pink radiology assistant made with love for Sama 💗🐾
Made with endless love by Mohamed ✨
"""
import os
from pathlib import Path
import streamlit as st

# 1. Basic config (must come first)
st.set_page_config(
    page_title="SemSemty AI 🌸",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. CSS + JS injection — keeps sidebar locked open
st.markdown("""
    <style>
        /* 💗 Made with love by Mohamed for Sama — always and forever 💗 */

        /* Hide the (X) close button inside the sidebar */
        [data-testid="stSidebar"] button[kind="header"] {
            display: none !important;
        }

        /* Keep the open/close arrow ALWAYS visible */
        [data-testid="collapsedControl"] {
            visibility: visible !important;
            opacity: 1 !important;
            display: flex !important;
        }

        /* Lock sidebar width on mobile and prevent slide-out */
        @media (max-width: 991.98px) {
            section[data-testid="stSidebar"] {
                width: 300px !important;
                position: fixed !important;
                z-index: 1000001 !important;
                transform: none !important;
                visibility: visible !important;
            }
        }
    </style>

    <script>
        // Force sidebar open on every load/rerun
        (function keepSidebarOpen() {
            function openSidebar() {
                // Streamlit stores sidebar state in localStorage
                const key = Object.keys(localStorage).find(k => k.includes('sidebar'));
                if (key) {
                    localStorage.setItem(key, 'expanded');
                }

                // If sidebar has collapsed class, click the toggle to reopen
                const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                const collapsed = window.parent.document.querySelector('[data-testid="collapsedControl"]');
                
                if (sidebar && sidebar.getAttribute('aria-expanded') === 'false' && collapsed) {
                    collapsed.click();
                }
            }

            // Run immediately and then watch for changes
            openSidebar();
            const observer = new MutationObserver(openSidebar);
            observer.observe(window.parent.document.body, { attributes: true, subtree: true });
        })();
    </script>
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
