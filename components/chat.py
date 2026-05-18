"""
components/chat.py — SemSemty AI Chat UI 🌸
Production UX version (no API key exposure, safe errors)
"""

import re
import random
import streamlit as st

from services.llm_service import chat_with_semsemty, text_to_speech
from constants.chat_data import QUICK_PROMPTS, REMINDERS, MODE_META


# ─────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────
def _is_arabic_dominant(text: str) -> bool:
    arabic = sum(1 for c in text if '\u0600' <= c <= '\u06ff')
    letters = sum(1 for c in text if c.isalpha())
    return arabic > 0 and letters > 0 and (arabic / letters) > 0.4


def format_bilingual(text: str) -> str:
    lines = text.split("\n")
    result = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
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

        if stripped.startswith(("#", "-", "*", ">", "|", "!")):
            result.append(line)
            continue

        if re.match(r"^\d+\.", stripped):
            result.append(line)
            continue

        if _is_arabic_dominant(stripped):
            result.append(f'<div class="arabic-line">{stripped}</div>')
        else:
            result.append(line)

    return "\n".join(result)


# ─────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────
def render_empty_state() -> None:
    mode = st.session_state.mode
    icon = MODE_META.get(mode, {}).get("icon", "🐾")
    color = MODE_META.get(mode, {}).get("color", "#FF5FA2")

    _, col, _ = st.columns([1, 3, 1])

    with col:
        st.markdown(
            f"""
            <div style="text-align:center;padding:2.5rem 0 1rem;">
                <div style="position:relative;display:inline-block;margin-bottom:1rem;">
                    <div style="position:absolute;top:50%;left:50%;
                        transform:translate(-50%,-50%);
                        width:110px;height:110px;border-radius:50%;
                        background:radial-gradient(circle,{color}35,transparent 70%);"></div>

                    <div style="font-size:5rem;line-height:1;
                        filter:drop-shadow(0 0 28px {color}99);
                        position:relative;z-index:1;">🐱</div>
                </div>

                <div style="font-family:Quicksand;font-weight:800;
                    font-size:2.2rem;margin-bottom:.4rem;">
                    SemSemty AI 🌸
                </div>

                <div style="color:rgba(255,182,217,0.7);font-size:.9rem;">
                    Your pink AI radiology bestie 🩻🐾
                </div>

                <div style="color:rgba(255,182,217,0.4);font-size:.75rem;margin-top:.5rem;">
                    Made with endless love by Mohamed 💗
                </div>

                <div style="margin-top:1rem;padding:.5rem;
                    border-radius:12px;
                    background:linear-gradient(135deg,{color}12,{color}06);
                    border:1px solid {color}33;
                    font-size:.8rem;">
                    {icon} Mode: <b>{mode}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# QUICK ACTIONS
# ─────────────────────────────────────────────
def render_quick_actions() -> None:
    mode = st.session_state.mode
    q_list = QUICK_PROMPTS.get(mode, [])

    if not q_list:
        return

    st.markdown(
        '<p style="text-align:center;color:rgba(255,182,217,.5);font-size:.75rem;">⚡ QUICK ACTIONS</p>',
        unsafe_allow_html=True,
    )

    row1 = q_list[:3]
    cols1 = st.columns(len(row1))

    for i, (label, msg) in enumerate(row1):
        with cols1[i]:
            if st.button(label, key=f"qa1_{i}", use_container_width=True):
                _fire_quick(msg)

    if len(q_list) > 3:
        row2 = q_list[3:6]
        cols2 = st.columns(len(row2))

        for i, (label, msg) in enumerate(row2):
            with cols2[i]:
                if st.button(label, key=f"qa2_{i}", use_container_width=True):
                    _fire_quick(msg)


def _fire_quick(msg: str) -> None:
    st.session_state.messages = []
    st.session_state.file_context = ""
    st.session_state.file_name = ""
    st.session_state.image_data = None
    st.session_state.pending_input = msg
    st.rerun()


# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────
def render_chat_history() -> None:
    for msg in st.session_state.messages:
        role = msg["role"]

        with st.chat_message(role, avatar="🐱" if role == "assistant" else "🩻"):
            content = msg.get("content", "")

            if isinstance(content, list):
                text_parts = [
                    b["text"]
                    for b in content
                    if isinstance(b, dict) and b.get("type") == "text"
                ]
                content = " ".join(text_parts)

            if role == "assistant":
                st.markdown(format_bilingual(content), unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="font-family:Quicksand;font-size:.95rem;">{content}</div>',
                    unsafe_allow_html=True,
                )


# ─────────────────────────────────────────────
# REMINDER SYSTEM
# ─────────────────────────────────────────────
def maybe_show_reminder(count: int) -> None:
    if count > 0 and count % 6 == 0:
        st.info(random.choice(REMINDERS))


# ─────────────────────────────────────────────
# FILE BANNER
# ─────────────────────────────────────────────
def render_file_banner() -> None:
    if st.session_state.get("file_name"):
        icon = "🔬" if st.session_state.get("image_data") else "📎"
        label = "Image ready for analysis" if icon == "🔬" else "File loaded"

        st.markdown(
            f"""
            <div style="padding:.6rem 1rem;
                border-radius:14px;
                background:linear-gradient(135deg,rgba(255,182,217,.1),rgba(201,184,255,.08));
                border:1px solid rgba(255,182,217,.3);
                margin-bottom:.6rem;">
                {icon} {label}: <b>{st.session_state.file_name}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# CHAT INPUT PIPELINE
# ─────────────────────────────────────────────
def handle_chat_input() -> None:
    render_file_banner()

    typed = st.chat_input("Ask SemSemty 🌸 | اسأليني أي حاجة 💕")

    user_text = None

    if st.session_state.get("pending_input"):
        user_text = st.session_state.pending_input
        st.session_state.pending_input = None
    elif typed:
        user_text = typed

    if not user_text:
        return

    image_data = st.session_state.get("image_data")
    has_image = image_data is not None

    with st.chat_message("user", avatar="🩻"):
        st.markdown(user_text)

    st.session_state.messages.append(
        {"role": "user", "content": user_text, "has_image": has_image}
    )
    st.session_state.total_messages += 1

    with st.chat_message("assistant", avatar="🐱"):
        with st.spinner("🌸 SemSemty is thinking..."):
            reply = chat_with_semsemty(
                messages=st.session_state.messages,
                mode=st.session_state.mode,
                mood=st.session_state.mood,
                extra_context=st.session_state.file_context,
                image_data=image_data,
                image_media_type=st.session_state.get(
                    "image_media_type", "image/jpeg"
                ),
            )

            st.markdown(format_bilingual(reply), unsafe_allow_html=True)

            # Voice
            if st.session_state.get("voice_output"):
                try:
                    st.audio(text_to_speech(reply), format="audio/mp3")
                except Exception:
                    pass

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

            st.session_state.image_data = None
            maybe_show_reminder(st.session_state.total_messages)
