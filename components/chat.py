"""
components/chat.py — SemSemty AI Chat UI 🌸
"""
import re
import random
import streamlit as st
from services.llm_service import chat_with_semsemty, text_to_speech
from constants.chat_data import QUICK_PROMPTS, REMINDERS, MODE_META


def _is_arabic_dominant(text: str) -> bool:
    arabic  = sum(1 for c in text if '\u0600' <= c <= '\u06ff')
    letters = sum(1 for c in text if c.isalpha())
    return arabic > 0 and letters > 0 and (arabic / letters) > 0.4


def format_bilingual(text: str) -> str:
    lines = text.split('\n')
    result = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        if in_code_block:
            result.append(line)
            continue
        stripped = line.strip()
        if not stripped:
            result.append(line)
            continue
        if stripped.startswith(('#', '-', '*', '>', '|', '!')):
            result.append(line)
            continue
        if re.match(r'^\d+\.', stripped):
            result.append(line)
            continue
        if _is_arabic_dominant(stripped):
            result.append(f'<div class="arabic-line">{stripped}</div>')
        else:
            result.append(line)
    return '\n'.join(result)


# ─────────────────────────────────────────────
# EMPTY STATE — rendered OUTSIDE any chat context
# ─────────────────────────────────────────────
def render_empty_state() -> None:
    mode  = st.session_state.mode
    icon  = MODE_META.get(mode, {}).get("icon", "🐾")
    color = MODE_META.get(mode, {}).get("color", "#FF5FA2")

    # Center column layout
    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown(
            f'<div style="text-align:center;padding:2.5rem 0 1rem;">'
            f'<div style="position:relative;display:inline-block;margin-bottom:1rem;">'
            f'<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);'
            f'width:110px;height:110px;border-radius:50%;'
            f'background:radial-gradient(circle,{color}35,transparent 70%);"></div>'
            f'<div class="heartbeat" style="font-size:5rem;line-height:1;display:inline-block;'
            f'filter:drop-shadow(0 0 28px {color}99);position:relative;z-index:1;">🐱</div>'
            f'</div>'
            f'<div class="gradient-text" style="font-family:Quicksand,sans-serif;font-weight:800;'
            f'font-size:2.4rem;line-height:1.1;margin-bottom:.4rem;">SemSemty AI 🌸</div>'
            f'<div style="color:rgba(255,182,217,0.6);font-size:.95rem;'
            f'font-family:Quicksand,sans-serif;font-weight:600;line-height:2;margin-bottom:.3rem;">'
            f'Your little pink AI kitty is here 🐾<br>'
            f'Ready to help you study radiology,<br>'
            f'cheer you up, and remind you how loved you are'
            f'</div>'
            f'<div style="color:rgba(255,182,217,0.3);font-size:.73rem;'
            f'font-style:italic;margin-bottom:1.5rem;">Made with endless love by Mohamed</div>',
            unsafe_allow_html=True,
        )

        if mode == "🔬 X-Ray Analyzer":
            st.markdown(
                f'<div style="background:linear-gradient(135deg,rgba(255,158,199,.12),rgba(201,184,255,.08));'
                f'border:1.5px solid rgba(255,182,217,.35);border-radius:18px;padding:.8rem 1.4rem;'
                f'font-size:.82rem;color:rgba(255,182,217,.8);font-weight:600;margin-bottom:1rem;line-height:2;">'
                f'🔬 <b style="color:#FF9EC7;">How to use X-Ray Analyzer:</b><br>'
                f'1. Upload your X-ray image in the sidebar<br>'
                f'2. Type your question or pick a quick action below<br>'
                f'3. I will give you a full educational analysis</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div style="background:linear-gradient(135deg,{color}12,{color}06);'
            f'border:1px solid {color}33;border-radius:18px;padding:.6rem 1.2rem;'
            f'font-size:.78rem;color:rgba(255,182,217,.5);font-family:Quicksand,sans-serif;'
            f'margin-bottom:.5rem;text-align:center;">'
            f'{icon} Currently in <b style="color:{color};">{mode}</b> mode</div>'
            f'</div>',   # close outer div
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# QUICK ACTIONS — pill buttons with full labels
# ─────────────────────────────────────────────
def render_quick_actions() -> None:
    mode   = st.session_state.mode
    q_list = QUICK_PROMPTS.get(mode, [])
    if not q_list:
        return

    pills = q_list[:6]

    st.markdown(
        '<p style="text-align:center;color:rgba(255,182,217,.45);'
        'font-size:.72rem;font-weight:700;letter-spacing:.06em;margin:.6rem 0 .4rem;">'
        '⚡ QUICK ACTIONS</p>',
        unsafe_allow_html=True,
    )

    # Row 1 — up to 3 pills
    row1 = pills[:3]
    cols1 = st.columns(len(row1))
    for i, (label, msg_text) in enumerate(row1):
        with cols1[i]:
            if st.button(label, key=f"qa_{mode}_{i}", use_container_width=True, help=msg_text):
                _fire_quick(msg_text)

    # Row 2 — remaining pills
    if len(pills) > 3:
        row2  = pills[3:6]
        cols2 = st.columns(len(row2))
        for i, (label, msg_text) in enumerate(row2):
            with cols2[i]:
                if st.button(label, key=f"qa_{mode}_{i+3}", use_container_width=True, help=msg_text):
                    _fire_quick(msg_text)

    st.markdown("<div style='margin-bottom:.6rem'></div>", unsafe_allow_html=True)


def _fire_quick(msg_text: str) -> None:
    st.session_state.messages         = []
    st.session_state.file_context     = ""
    st.session_state.file_name        = ""
    st.session_state.image_data       = None
    st.session_state.image_media_type = "image/jpeg"
    st.session_state.pending_input    = msg_text
    st.rerun()


# ─────────────────────────────────────────────
# CHAT HISTORY — only called when messages exist
# ─────────────────────────────────────────────
def render_chat_history() -> None:
    for msg in st.session_state.messages:
        role = msg["role"]
        with st.chat_message(role, avatar="🐱" if role == "assistant" else "🩻"):
            content = msg.get("content", "")
            if isinstance(content, list):
                text_parts = [b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text"]
                content = " ".join(text_parts)
            if role == "assistant":
                st.markdown(format_bilingual(content), unsafe_allow_html=True)
            else:
                if msg.get("has_image"):
                    st.markdown("📷 *[Image uploaded for analysis]*")
                st.markdown(
                    f'<div style="direction:auto;unicode-bidi:plaintext;'
                    f'font-family:Quicksand,Tajawal,sans-serif;font-size:.95rem;'
                    f'color:rgba(255,193,218,0.9);">{content}</div>',
                    unsafe_allow_html=True,
                )


def maybe_show_reminder(count: int) -> None:
    if count > 0 and count % 6 == 0:
        st.info(random.choice(REMINDERS))


def render_file_banner() -> None:
    if st.session_state.get("file_name"):
        is_image = st.session_state.get("image_data") is not None
        icon     = "🔬" if is_image else "📎"
        label    = "Image ready for analysis" if is_image else "Loaded"
        st.markdown(
            f'<div style="background:linear-gradient(135deg,rgba(255,182,217,.1),rgba(201,184,255,.08));'
            f'border:1.5px solid rgba(255,182,217,.3);border-radius:18px;'
            f'padding:.6rem 1.2rem;margin-bottom:.8rem;font-size:.82rem;color:rgba(255,182,217,.7);'
            f'backdrop-filter:blur(10px);">'
            f'{icon} {label}: <b style="color:#FF5FA2;">{st.session_state.file_name}</b>'
            f' — Ask me anything about it!</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# CHAT INPUT — main message pipeline
# ─────────────────────────────────────────────
def handle_chat_input() -> None:
    render_file_banner()
    typed = st.chat_input("Ask me anything Semsem 🌸  |  اسأليني أي حاجة 💕")

    user_text = None
    if st.session_state.pending_input:
        user_text                      = st.session_state.pending_input
        st.session_state.pending_input = None
    elif typed:
        user_text = typed

    if not user_text:
        return

    image_data       = st.session_state.get("image_data")
    image_media_type = st.session_state.get("image_media_type", "image/jpeg")
    has_image        = image_data is not None

    with st.chat_message("user", avatar="🩻"):
        if has_image:
            st.markdown("📷 *[Image uploaded for analysis]*")
        st.markdown(
            f'<div style="direction:auto;unicode-bidi:plaintext;'
            f'font-family:Quicksand,Tajawal,sans-serif;font-size:.95rem;'
            f'color:rgba(255,193,218,0.9);">{user_text}</div>',
            unsafe_allow_html=True,
        )

    st.session_state.messages.append({"role": "user", "content": user_text, "has_image": has_image})
    st.session_state.total_messages += 1

    with st.chat_message("assistant", avatar="🐱"):
        with st.spinner("🌸 SemSemty is thinking... 🐾"):
            try:
                reply = chat_with_semsemty(
                    messages         = st.session_state.messages,
                    mode             = st.session_state.mode,
                    mood             = st.session_state.mood,
                    extra_context    = st.session_state.file_context,
                    image_data       = image_data,
                    image_media_type = image_media_type,
                )
                st.markdown(format_bilingual(reply), unsafe_allow_html=True)

                if st.session_state.voice_output:
                    try:
                        st.audio(text_to_speech(reply), format="audio/mp3")
                    except Exception:
                        pass

                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.image_data = None
                maybe_show_reminder(st.session_state.total_messages)

            except Exception as e:
                err = str(e)
                if "rate_limit" in err.lower() or "429" in err:
                    st.warning("⏳ Rate limit — wait a moment and try again 💗")
                elif "overloaded" in err.lower():
                    st.warning("⏳ Server busy — try again in a moment 🌸")
                elif any(x in err.lower() for x in ("api_key", "authentication", "missing", "invalid_api_key", "forbidden", "403")):
                    st.error("🔑 Groq API Key error — check GROQ_API_KEY in your .env file 💗")
                else:
                    st.error(f"😔 Error: `{err}`")
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()
