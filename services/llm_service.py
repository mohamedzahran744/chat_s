"""
services/llm_service.py — Groq API + gTTS voice for SemSemty AI
Clean production version (no dotenv, no fallback, no UI keys)
"""

import io
import re
import base64
import os
import urllib.request
import json

from constants.chat_data import GROQ_MODEL, MAX_TOKENS, TEMPERATURE
from constants.system_prompt import get_system_prompt


# ─────────────────────────────────────────────
# API KEY (ONLY SOURCE OF TRUTH)
# ─────────────────────────────────────────────
def _get_api_key() -> str:
    """
    Reads API key ONLY from environment variables.
    Works on:
    - Streamlit Cloud Secrets
    - local environment variables
    """
    key = os.getenv("GROQ_API_KEY")

    if not key:
        raise ValueError(
            "❌ GROQ_API_KEY is missing.\n"
            "Add it in Streamlit Secrets or environment variables."
        )

    return key.strip().strip('"').strip("'")


# ─────────────────────────────────────────────
# MAIN CHAT FUNCTION
# ─────────────────────────────────────────────
def chat_with_semsemty(
    messages: list[dict],
    mode: str,
    mood: str,
    extra_context: str = "",
    image_data: bytes | None = None,
    image_media_type: str = "image/jpeg",
) -> str:

    api_key = _get_api_key()
    system = get_system_prompt(mode, mood)

    if extra_context:
        system += f"\n\n[UPLOADED CONTEXT]\n{extra_context}\n[END]"

    # ── Clean messages ─────────────────────────
    clean_messages = [
        {"role": m["role"], "content": str(m.get("content", ""))}
        for m in messages
        if m.get("role") in ("user", "assistant")
    ]

    clean_messages = clean_messages[-30:]  # limit context

    # ── Vision support ─────────────────────────
    if image_data and clean_messages and clean_messages[-1]["role"] == "user":
        b64 = base64.standard_b64encode(image_data).decode("utf-8")
        data_url = f"data:{image_media_type};base64,{b64}"

        clean_messages[-1] = {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": data_url},
                },
                {
                    "type": "text",
                    "text": clean_messages[-1]["content"]
                    or "Please analyze this image.",
                },
            ],
        }

        model = "meta-llama/llama-4-scout-17b-16e-instruct"
    else:
        model = GROQ_MODEL

    # ── Payload ────────────────────────────────
    payload = {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "messages": [
            {"role": "system", "content": system}
        ] + clean_messages,
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        raise RuntimeError(f"❌ Groq API error: {str(e)}")


# ─────────────────────────────────────────────
# TEXT TO SPEECH
# ─────────────────────────────────────────────
def text_to_speech(text: str) -> bytes:
    from gtts import gTTS

    sample = text[:100]

    lang = (
        "en"
        if any(c.isascii() and c.isalpha() for c in sample)
        and not any("\u0600" <= c <= "\u06ff" for c in sample)
        else "ar"
    )

    clean = re.sub(r"```[\s\S]*?```", " code block ", text)
    clean = re.sub(r"`[^`]+`", "", clean)
    clean = re.sub(r"[#*_~>\[\]()]", "", clean).strip()[:2000]

    tts = gTTS(text=clean, lang=lang, slow=False)

    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)

    return buf.read()