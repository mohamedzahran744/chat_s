"""
SemSemty AI 🌸 — A cute pink radiology assistant made with love for Sama 💗🐾
Made with endless love by Mohamed ✨
"""
import os
from pathlib import Path
import streamlit as st

# 1. الإعدادات الأساسية (يجب أن تكون في البداية)
st.set_page_config(
    page_title="SemSemty AI 🌸",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded", # إجبار الحالة الأولية على التمدد
)

# 2. حقن CSS لإجبار الشريط الجانبي على البقاء مفتوحاً ومنع إغلاقه
st.markdown("""
    <style>
        /* إخفاء زر الإغلاق (X) داخل الشريط الجانبي */
        [data-testid="stSidebar"] button[kind="header"] {
            display: none !important;
        }
        
        /* إخفاء زر الفتح (السهيم) في حال حاول النظام إغلاقه */
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* تثبيت عرض الشريط الجانبي ومنع اختفائه على الشاشات الصغيرة */
        @media (max-width: 991.98px) {
            section[data-testid="stSidebar"] {
                width: 300px !important;
                position: fixed !important;
                z-index: 1000001 !important;
                transform: none !important; /* يمنع حركة الـ Slide-out */
                visibility: visible !important;
            }
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
# تمرير نسخة من الـ session_state للدالة
sidebar_out = render_sidebar(dict(st.session_state))

# تحديث القيم بناءً على تفاعل المستخدم في السايدبار
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
