"""
components/sidebar.py — SemSemty AI Pink Sidebar 🌸
API key is loaded automatically from .env — no user input needed.
"""
import random
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
  <div style="color:rgba(255,182,217,0.35);font-size:.62rem;font-family:'Quicksand',sans-serif;
    font-style:italic;margin-bottom:.7rem;">Made with endless love for Sama 💕</div>
  <span style="background:linear-gradient(135deg,rgba(52,211,153,0.15),rgba(52,211,153,0.08));
    color:#34d399;font-size:.62rem;font-weight:800;padding:3px 12px;border-radius:999px;
    border:1.5px solid rgba(52,211,153,0.3);font-family:'Quicksand',sans-serif;">
    ● Online for Sama 🌸</span>
</div>
""", unsafe_allow_html=True)

        st.divider()

        # ── Mode ──────────────────────────────────────────────────
        _label("Mode", "🩻")
        mode  = st.radio("mode_radio", MODES,
                         index=MODES.index(state.get("mode", MODES[0])),
                         label_visibility="collapsed")
        meta  = MODE_META.get(mode, {})
        color = meta.get("color", "#FF5FA2")
        if meta:
            _mode_card(meta.get("desc", ""), color)

        st.divider()

        # ── Mood ──────────────────────────────────────────────────
        _label("How are you feeling?", "💕")
        mood = st.radio("mood_radio", MOODS,
                        index=MOODS.index(state.get("mood", MOODS[0])),
                        label_visibility="collapsed")

        mood_msgs = {
            "😊 Happy":       ("Yay! Happy Sama!",      "Full pink energy today 🌸"),
            "😴 Sleepy":      ("Rest mode on!",          "I'll be extra gentle 💕"),
            "📚 Study Mode":  ("Study queen activated!", "Let's ace radiology 🩻"),
            "💖 Need Love":   ("Come here for hugs!",   "You're so loved Semsem 💗"),
        }
        title, sub = mood_msgs.get(mood, ("", ""))
        if title:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{color}18,{color}08);'
                f'border:1px solid {color}44;border-radius:12px;padding:.4rem .8rem;'
                f'font-size:.72rem;color:rgba(255,182,217,0.7);margin-top:.3rem;font-weight:700;">'
                f'<b style="color:{color};">{title}</b> {sub}</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Voice ─────────────────────────────────────────────────
        _label("Voice Replies", "🔊")
        voice_output = st.toggle("Auto voice output 🔊", value=state.get("voice_output", False))

        st.divider()

        # ── File / Image Upload ───────────────────────────────────
        is_xray_mode = (mode == "🔬 X-Ray Analyzer")

        if is_xray_mode:
            _label("Upload X-Ray / Scan Image", "🔬")
            st.caption("10 MB max • PNG, JPG, WEBP — X-rays, CT, MRI")
            uploaded = st.file_uploader(
                "xray_upload",
                type=["png", "jpg", "jpeg", "webp"],
                label_visibility="collapsed",
                key="xray_uploader",
            )
        else:
            _label("Upload Lecture / Notes", "📎")
            st.caption("10 MB max • PDF, DOCX, TXT, images")
            uploaded = st.file_uploader(
                "doc_upload",
                type=["pdf","docx","txt","md","py","cpp","c","h","js","ts",
                      "java","json","csv","xml","html","css","sql","yaml","yml",
                      "png","jpg","jpeg","webp","gif"],
                label_visibility="collapsed",
                key="doc_uploader",
            )

        if uploaded:
            result = extract_text_from_file(uploaded)
            if len(result) == 4:
                extracted, label_type, img_bytes, img_media_type = result
                st.session_state.image_data       = img_bytes
                st.session_state.image_media_type = img_media_type
                st.session_state.file_context     = build_file_context(extracted, label_type, uploaded.name)
                st.session_state.file_name        = uploaded.name
                st.session_state.total_files     += 1
                st.success(f"✅ Ready for analysis: **{uploaded.name}** 🔬")
                st.image(uploaded, caption=f"🔬 {uploaded.name}", use_container_width=True)
            else:
                extracted, label_type = result
                st.session_state.file_context = build_file_context(extracted, label_type, uploaded.name)
                st.session_state.file_name    = uploaded.name
                st.session_state.image_data   = None
                st.session_state.total_files += 1
                st.success(f"✅ **{uploaded.name}** loaded 🌸")

        if st.session_state.get("file_name"):
            st.markdown(
                f'<div style="background:linear-gradient(135deg,rgba(255,182,217,0.1),rgba(201,184,255,0.08));'
                f'border:1.5px solid rgba(255,182,217,0.25);border-radius:14px;'
                f'padding:.45rem .9rem;font-size:.75rem;color:rgba(255,182,217,0.7);margin-top:.4rem;">'
                f'📎 <b style="color:#FF5FA2;">{st.session_state.file_name}</b></div>',
                unsafe_allow_html=True,
            )
            if st.button("🗑️ Remove file", use_container_width=True, key="remove_file"):
                st.session_state.file_context     = ""
                st.session_state.file_name        = ""
                st.session_state.image_data       = None
                st.session_state.image_media_type = "image/jpeg"
                st.rerun()

        st.divider()

        # ── API key status (read-only indicator, no input) ────────
        import os
        groq_key = os.getenv("GROQ_API_KEY", "").strip().strip('"').strip("'")
        if groq_key:
            st.markdown(
                '<div style="background:linear-gradient(135deg,rgba(52,211,153,0.12),rgba(52,211,153,0.06));'
                'border:1px solid rgba(52,211,153,0.3);border-radius:12px;padding:.4rem .8rem;'
                'font-size:.72rem;color:#34d399;font-weight:700;">'
                '🔑 Groq API connected ✓</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="background:rgba(255,95,100,0.1);border:1px solid rgba(255,95,100,0.3);'
                'border-radius:12px;padding:.4rem .8rem;font-size:.72rem;color:#ff9999;font-weight:700;">'
                '⚠️ Add GROQ_API_KEY to .env file</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Stats ─────────────────────────────────────────────────
        _label("Stats", "📊")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("💬 Messages", state.get("total_messages", 0))
        with c2:
            st.metric("📁 Files", state.get("total_files", 0))

        msgs  = state.get("total_messages", 0)
        level = ("🌱 Beginner"       if msgs < 5  else
                 "⭐ Explorer"        if msgs < 20 else
                 "🔥 Study Queen"    if msgs < 50 else
                 "👑 Radiology Legend")
        st.markdown(
            f'<div style="text-align:center;margin-top:.4rem;'
            f'background:linear-gradient(135deg,rgba(255,182,217,0.08),rgba(201,184,255,0.06));'
            f'border:1px solid rgba(255,182,217,0.2);border-radius:12px;padding:.4rem;'
            f'font-size:.73rem;color:rgba(255,182,217,0.6);font-weight:700;">'
            f'Level: <span style="color:#FF5FA2;">{level}</span></div>',
            unsafe_allow_html=True,
        )

        st.divider()

        clear = st.button("🗑️ Clear Chat", use_container_width=True)

        # ── Daily Love Message ────────────────────────────────────
        st.divider()
        today_msg = LOVE_MESSAGES[hash(str(__import__('datetime').date.today())) % len(LOVE_MESSAGES)]
        st.markdown(f'<div class="secret-msg">{today_msg}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("💌 Open when tired, Semsem", expanded=False):
            st.markdown("""
<div style="text-align:center;padding:1rem .5rem;">
  <div class="heartbeat" style="font-size:2.8rem;display:inline-block;">💗</div>
  <div class="gradient-text" style="font-weight:800;font-size:1.1rem;margin:.5rem 0 .3rem;
    font-family:'Quicksand',sans-serif;">Mohamed loves Sama</div>
  <div style="color:rgba(255,182,217,0.6);font-size:.83rem;line-height:2.2;
    font-family:'Quicksand',sans-serif;">
    محمد بيحبك يا سما 💖<br>
    إنتي أجمل وأشطر بنت في الدنيا 🌸<br>
    كل سطر في الابليكيشن ده اتكتب بحبك ✨<br>
    هو فخور بيكي كل يوم 💗<br>
    You are his favorite person 🐾
  </div>
  <div style="margin-top:.8rem;font-size:1.6rem;animation:floatAnim 2s ease-in-out infinite;
    display:inline-block;">💗 🌸 🐱 ✨ 💕</div>
</div>
""", unsafe_allow_html=True)

        # ── Footer ────────────────────────────────────────────────
        st.markdown(f"""
<div style="text-align:center;padding:.9rem 0 .5rem;font-family:'Quicksand',sans-serif;">
  <div style="color:rgba(255,182,217,0.35);font-size:.63rem;line-height:2.2;">
    Made with endless love by Mohamed 💗<br>
    For Sama — the cutest future radiologist 🩻🐾<br>
    <span style="color:rgba(201,184,255,0.5);font-weight:800;">Powered by Groq + Llama ✨</span><br>
    <span style="opacity:.3;font-size:.57rem;">v{APP_VERSION}</span>
  </div>
</div>""", unsafe_allow_html=True)

    return {
        "mode":          mode,
        "mood":          mood,
        "voice_output":  voice_output,
        "clear":         clear,
        "pending_voice": None,
    }
