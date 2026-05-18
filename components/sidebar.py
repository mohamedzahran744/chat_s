import os
import streamlit as st
from constants.chat_data import APP_VERSION, MODES, MOODS, MODE_META, LOVE_MESSAGES
from components.file_handler import extract_text_from_file, build_file_context

def _label(text: str, emoji: str = "") -> None:
    st.markdown(
        f'<p style="color:rgba(255,182,217,0.6);font-size:.68rem;font-weight:800;'
        f'margin:0 0 6px;letter-spacing:.08em;text-transform:uppercase;">'
        f'{emoji} {text}</p>',
        unsafe_allow_html=True,
    )

def _mode_card(desc: str, color: str) -> None:
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{color}18,{color}08);'
        f'border:1px solid {color}44;border-radius:14px;'
        f'padding:.5rem .9rem;font-size:.73rem;color:rgba(255,182,217,0.7);'
        f'margin-top:.3rem;font-family:Quicksand,sans-serif;font-weight:600;line-height:1.7;">'
        f'{desc}</div>',
        unsafe_allow_html=True,
    )

def render_sidebar(state: dict) -> dict:
    # ── هُنا الحل الجذري لإبقاء الشريط ظاهراً دائماً ──
    st.markdown("""
        <style>
            /* إخفاء زر الإغلاق الداخلي (X) */
            [data-testid="stSidebar"] button[kind="header"] {
                display: none !important;
            }
            
            /* إخفاء زر الفتح (الذي يظهر في الزاوية عند الانغلاق) */
            [data-testid="collapsedControl"] {
                display: none !important;
            }

            /* إجبار الشريط الجانبي على البقاء مفتوحاً ومنع تصغيره */
            section[data-testid="stSidebar"] {
                width: 330px !important;
                margin-left: 0 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # ملاحظة: تأكد من ضبط initial_sidebar_state="expanded" في st.set_page_config بملف main.py
    
    with st.sidebar:
        # ── Header ────────────────────────────────────────────────
        st.markdown("""
<div style="text-align:center;padding:1.5rem 0 1rem;">
  <div style="position:relative;display:inline-block;margin-bottom:.3rem;">
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
      width:80px;height:80px;border-radius:50%;
      background:linear-gradient(135deg,rgba(255,95,162,0.25),rgba(201,184,255,0.2));
      animation:pulse-ring 2.5s ease-out infinite;"></div>
    <div class="heartbeat" style="font-size:3.2rem;line-height:1;display:inline-block;
      filter:drop-shadow(0 4px 18px rgba(255,95,162,0.5));position:relative;z-index:1;">🐱</div>
  </div>
  <div class="gradient-text" style="font-family:'Quicksand',sans-serif;
    font-weight:800;font-size:1.9rem;margin:.3rem 0 .05rem;line-height:1;">SemSemty AI</div>
  <div style="color:rgba(255,182,217,0.6);font-size:.72rem;font-family:'Quicksand',sans-serif;
    font-weight:600;margin-bottom:.5rem;">Your Pink Radiology Bestie 🩻🐾</div>
  <span style="background:linear-gradient(135deg,rgba(52,211,153,0.15),rgba(52,211,153,0.08));
    color:#34d399;font-size:.62rem;font-weight:800;padding:3px 12px;border-radius:999px;
    border:1.5px solid rgba(52,211,153,0.3);font-family:'Quicksand',sans-serif;">
    ● Online for Sama 🌸</span>
</div>
""", unsafe_allow_html=True)

        st.divider()

        # ── Mode Selection ────────────────────────────────────────
        _label("Mode", "🩻")
        mode = st.radio("mode_radio", MODES,
                        index=MODES.index(state.get("mode", MODES[0])),
                        label_visibility="collapsed")
        meta = MODE_META.get(mode, {})
        color = meta.get("color", "#FF5FA2")
        if meta:
            _mode_card(meta.get("desc", ""), color)

        st.divider()

        # ── Mood Selection ────────────────────────────────────────
        _label("How are you feeling?", "💕")
        mood = st.radio("mood_radio", MOODS,
                        index=MOODS.index(state.get("mood", MOODS[0])),
                        label_visibility="collapsed")

        st.divider()

        # ── File Upload ──────────────────────────────────────────
        is_xray_mode = (mode == "🔬 X-Ray Analyzer")
        _label("Upload Scan" if is_xray_mode else "Upload Notes", "📎")
        
        uploaded = st.file_uploader(
            "uploader",
            type=["png", "jpg", "jpeg", "webp", "pdf", "docx", "txt"],
            label_visibility="collapsed",
            key="doc_uploader"
        )

        if uploaded:
            # منطق معالجة الملف (يفترض وجود الدوال المستوردة)
            st.success(f"✅ {uploaded.name} Loaded")

        st.divider()

        # ── Footer ────────────────────────────────────────────────
        st.markdown(f"""
<div style="text-align:center;padding:.9rem 0 .5rem;font-family:'Quicksand',sans-serif;">
  <div style="color:rgba(255,182,217,0.35);font-size:.63rem;line-height:2.2;">
    Made with love by Mohamed 💗<br>
    For Sama 🩻🐾<br>
    <span style="opacity:.3;font-size:.57rem;">v{APP_VERSION}</span>
  </div>
</div>""", unsafe_allow_html=True)

    return {
        "mode": mode,
        "mood": mood,
        "voice_output": state.get("voice_output", False),
        "clear": False,
        "pending_voice": None,
    }
