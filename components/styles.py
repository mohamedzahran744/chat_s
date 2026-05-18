"""
components/styles.py — Full pink dreamy CSS for SemSemty AI 🌸
Falling sakura, floating hearts, glassmorphism, cat animations
"""
import streamlit as st


def inject_css() -> None:
    st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700;800&family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">

<style>
/* ═══════════════════════════════════════════
   SEMSEMTY AI — PINK DREAMY WORLD 🌸
   ═══════════════════════════════════════════ */

:root {
  --baby-pink:    #FFD6EA;
  --soft-rose:    #FFB3D4;
  --heart-pink:   #FF5FA2;
  --pastel-pink:  #FFE8F2;
  --cream:        #FFF8FC;
  --blush:        #FFCCE5;
  --lilac:        #EAD9FF;
  --sky:          #D4F0FF;
  --text-main:    #FFE0EF;
  --text-soft:    #FFB6D9;
  --text-muted:   #FFCCE5;
  --glass-bg:     rgba(80, 20, 50, 0.65);
  --glass-border: rgba(255, 150, 200, 0.45);
  --shadow-pink:  rgba(255, 95, 162, 0.2);
}

/* ── Root / Body ── */
html, body, [data-testid="stApp"] {
  background: linear-gradient(135deg, #3D1030 0%, #2A0820 40%, #301545 100%) !important;
  font-family: 'Quicksand', sans-serif !important;
  color: var(--text-main) !important;
}

/* Animated mesh background */
[data-testid="stApp"]::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(ellipse 60% 40% at 20% 30%, rgba(255, 107, 157, 0.28) 0%, transparent 70%),
    radial-gradient(ellipse 50% 60% at 80% 70%, rgba(201, 184, 255, 0.22) 0%, transparent 70%),
    radial-gradient(ellipse 40% 50% at 50% 10%, rgba(255, 182, 217, 0.20) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
  animation: bgPulse 8s ease-in-out infinite;
}

@keyframes bgPulse {
  0%, 100% { opacity: 0.8; }
  50%       { opacity: 1; }
}

/* ── Sakura Petals ── */
.sakura-container {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.petal {
  position: absolute;
  top: -30px;
  width: 10px; height: 10px;
  border-radius: 50% 0 50% 0;
  opacity: 0;
  animation: petalFall linear infinite;
}

.petal:nth-child(1)  { left:5%;   background:#FFB6D9; width:8px;  height:8px;  animation-duration:8s;  animation-delay:0s;   }
.petal:nth-child(2)  { left:15%;  background:#FFC1DA; width:12px; height:12px; animation-duration:10s; animation-delay:1s;   }
.petal:nth-child(3)  { left:25%;  background:#FF9EC7; width:7px;  height:7px;  animation-duration:7s;  animation-delay:2s;   }
.petal:nth-child(4)  { left:35%;  background:#FFE4F1; width:10px; height:10px; animation-duration:9s;  animation-delay:0.5s; }
.petal:nth-child(5)  { left:45%;  background:#FFB6D9; width:9px;  height:9px;  animation-duration:11s; animation-delay:3s;   }
.petal:nth-child(6)  { left:55%;  background:#FFC1DA; width:11px; height:11px; animation-duration:8s;  animation-delay:1.5s; }
.petal:nth-child(7)  { left:65%;  background:#FF9EC7; width:8px;  height:8px;  animation-duration:10s; animation-delay:2.5s; }
.petal:nth-child(8)  { left:75%;  background:#FFE4F1; width:7px;  height:7px;  animation-duration:9s;  animation-delay:0.8s; }
.petal:nth-child(9)  { left:85%;  background:#FFB6D9; width:12px; height:12px; animation-duration:12s; animation-delay:4s;   }
.petal:nth-child(10) { left:92%;  background:#FFC1DA; width:9px;  height:9px;  animation-duration:7s;  animation-delay:1.8s; }
.petal:nth-child(11) { left:10%;  background:#FF5FA2; width:6px;  height:6px;  animation-duration:8s;  animation-delay:5s;   }
.petal:nth-child(12) { left:40%;  background:#FFB6D9; width:10px; height:10px; animation-duration:11s; animation-delay:3.5s; }
.petal:nth-child(13) { left:70%;  background:#FFC1DA; width:8px;  height:8px;  animation-duration:9s;  animation-delay:2.2s; }
.petal:nth-child(14) { left:88%;  background:#FF9EC7; width:11px; height:11px; animation-duration:10s; animation-delay:6s;   }
.petal:nth-child(15) { left:50%;  background:#FFE4F1; width:7px;  height:7px;  animation-duration:8s;  animation-delay:4.5s; }

@keyframes petalFall {
  0%   { transform: translateY(-30px) rotate(0deg)   translateX(0);   opacity: 0; }
  10%  { opacity: 0.7; }
  90%  { opacity: 0.4; }
  100% { transform: translateY(110vh)  rotate(720deg) translateX(60px); opacity: 0; }
}

/* ── Floating Hearts ── */
.hearts-container {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.heart {
  position: absolute;
  bottom: -30px;
  font-size: 14px;
  opacity: 0;
  animation: heartFloat linear infinite;
}

.heart:nth-child(1) { left:8%;   font-size:12px; animation-duration:7s;  animation-delay:0s;   }
.heart:nth-child(2) { left:20%;  font-size:16px; animation-duration:9s;  animation-delay:2s;   }
.heart:nth-child(3) { left:35%;  font-size:10px; animation-duration:8s;  animation-delay:4s;   }
.heart:nth-child(4) { left:50%;  font-size:14px; animation-duration:11s; animation-delay:1s;   }
.heart:nth-child(5) { left:65%;  font-size:12px; animation-duration:7s;  animation-delay:3s;   }
.heart:nth-child(6) { left:78%;  font-size:18px; animation-duration:10s; animation-delay:5s;   }
.heart:nth-child(7) { left:90%;  font-size:11px; animation-duration:8s;  animation-delay:0.5s; }
.heart:nth-child(8) { left:42%;  font-size:15px; animation-duration:9s;  animation-delay:6s;   }

@keyframes heartFloat {
  0%   { transform: translateY(0)      rotate(-15deg) scale(0.8); opacity: 0;   }
  10%  { opacity: 0.6; }
  50%  { transform: translateY(-50vh)  rotate(15deg)  scale(1);   opacity: 0.4; }
  90%  { opacity: 0.1; }
  100% { transform: translateY(-110vh) rotate(-10deg) scale(0.6); opacity: 0;   }
}

/* ── Floating Cats ── */
.cats-container {
  position: fixed;
  pointer-events: none;
  z-index: 1;
}

.cat-float {
  position: fixed;
  font-size: 24px;
  opacity: 0.15;
  animation: catFloat ease-in-out infinite;
}

.cat-float:nth-child(1) { bottom: 20%; right: 3%;  animation-duration: 6s;  animation-delay: 0s;   }
.cat-float:nth-child(2) { bottom: 50%; left:  2%;  animation-duration: 8s;  animation-delay: 2s;   font-size: 18px; }
.cat-float:nth-child(3) { top:    15%; right: 5%;  animation-duration: 7s;  animation-delay: 4s;   font-size: 20px; }

@keyframes catFloat {
  0%, 100% { transform: translateY(0)    rotate(-5deg); opacity: 0.12; }
  50%       { transform: translateY(-20px) rotate(5deg);  opacity: 0.2;  }
}

/* ── Main content area ── */
[data-testid="stMain"] {
  background: transparent !important;
  position: relative;
  z-index: 2;
}

.main .block-container {
  padding-top: 1.5rem !important;
  max-width: 900px !important;
  margin: 0 auto !important;
  background: transparent !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(26,5,16,0.97) 0%, rgba(15,2,10,0.99) 100%) !important;
  border-right: 1.5px solid rgba(255,182,217,0.15) !important;
  backdrop-filter: blur(20px);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown p {
  color: #FFCCE5 !important;
  font-family: 'Quicksand', sans-serif !important;
}

/* ── Gradient text ── */
.gradient-text {
  background: linear-gradient(135deg, #FF9EC7 0%, #FFB6D9 40%, #C9B8FF 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ── Heartbeat animation ── */
.heartbeat {
  animation: heartbeat 1.5s ease-in-out infinite;
  display: inline-block;
}
@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  14%       { transform: scale(1.15); }
  28%       { transform: scale(1); }
  42%       { transform: scale(1.1); }
  56%       { transform: scale(1); }
}

/* ── Pulse ring ── */
@keyframes pulse-ring {
  0%   { transform: translate(-50%,-50%) scale(0.8); opacity: 0.8; }
  100% { transform: translate(-50%,-50%) scale(1.8); opacity: 0; }
}

/* ── Float animation ── */
@keyframes floatAnim {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-8px); }
}

/* ── Slide up ── */
@keyframes slideUp {
  from { transform: translateY(12px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}

/* ── Blink dots ── */
.blink {
  animation: blink 1.4s ease-in-out infinite;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.2; }
}

/* ── Sparkle ── */
.sparkle {
  animation: sparkle 2s ease-in-out infinite;
  display: inline-block;
}
@keyframes sparkle {
  0%, 100% { transform: scale(1)    rotate(0deg);   opacity: 1;   }
  50%       { transform: scale(1.3) rotate(180deg); opacity: 0.6; }
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
  background: rgba(70, 15, 40, 0.7) !important;
  border: 1px solid rgba(255,150,200,0.35) !important;
  border-radius: 20px !important;
  backdrop-filter: blur(12px) !important;
  margin-bottom: 0.8rem !important;
  animation: slideUp 0.3s ease both !important;
  box-shadow: 0 4px 20px rgba(255,95,162,0.15) !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] li {
  color: #FFD6EA !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
  background: rgba(255, 240, 248, 0.08) !important;
  border: 1.5px solid rgba(255, 182, 217, 0.3) !important;
  border-radius: 28px !important;
  backdrop-filter: blur(16px) !important;
}

[data-testid="stChatInput"] textarea {
  background: transparent !important;
  color: var(--pastel-pink) !important;
  font-family: 'Quicksand', sans-serif !important;
  font-size: 0.9rem !important;
}

[data-testid="stChatInput"] textarea::placeholder {
  color: rgba(255, 182, 217, 0.4) !important;
}

/* ── Buttons — high contrast, always visible ── */
.stButton > button {
  background: linear-gradient(135deg, rgba(255,95,162,0.22), rgba(180,140,255,0.18)) !important;
  border: 1.5px solid rgba(255,150,200,0.55) !important;
  border-radius: 20px !important;
  color: #FFCCE5 !important;
  fill: #FFCCE5 !important;
  font-family: 'Quicksand', sans-serif !important;
  font-weight: 800 !important;
  font-size: 0.85rem !important;
  backdrop-filter: blur(8px) !important;
  transition: all 0.25s ease !important;
  letter-spacing: 0.02em !important;
  text-shadow: 0 1px 8px rgba(255,95,162,0.4) !important;
  min-height: 3rem !important;
  padding: 0.5rem 1rem !important;
  -webkit-text-fill-color: #FFCCE5 !important;
}

/* Every possible child element inside button */
.stButton > button *,
.stButton > button p,
.stButton > button span,
.stButton > button div,
.stButton > button small,
.stButton > button strong {
  color: #FFCCE5 !important;
  -webkit-text-fill-color: #FFCCE5 !important;
  font-weight: 800 !important;
  opacity: 1 !important;
  visibility: visible !important;
}

.stButton > button:hover {
  background: linear-gradient(135deg, rgba(255,95,162,0.38), rgba(180,140,255,0.32)) !important;
  border-color: rgba(255,95,162,0.75) !important;
  transform: translateY(-3px) scale(1.02) !important;
  box-shadow: 0 8px 24px rgba(255,95,162,0.35) !important;
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
}

.stButton > button:hover *,
.stButton > button:hover p,
.stButton > button:hover span,
.stButton > button:hover div {
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
}

/* ── Radio buttons ── */
.stRadio > div {
  gap: 0.4rem !important;
}
.stRadio > div > label {
  background: rgba(255,240,248,0.06) !important;
  border: 1px solid rgba(255,182,217,0.2) !important;
  border-radius: 14px !important;
  padding: 0.4rem 0.8rem !important;
  transition: all 0.2s ease !important;
  cursor: pointer !important;
}
.stRadio > div > label:hover {
  border-color: rgba(255,95,162,0.4) !important;
  background: rgba(255,95,162,0.08) !important;
}
.stRadio > div > label[data-baseweb="radio"] > div:first-child {
  background-color: #FF5FA2 !important;
  border-color: #FF5FA2 !important;
}

/* ── Toggle ── */
.stToggle > label > div[data-checked="true"] {
  background: linear-gradient(135deg, #FF5FA2, #C9B8FF) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
  background: rgba(255,240,248,0.06) !important;
  border: 1px solid rgba(255,182,217,0.25) !important;
  border-radius: 14px !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: transparent !important;
  border: none !important;
}
[data-testid="stFileUploader"] > label[data-visibility="hidden"] {
  display: none !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
}
[data-testid="stFileUploaderDropzone"] {
  background: rgba(255,240,248,0.04) !important;
  border: 1.5px dashed rgba(255,182,217,0.3) !important;
  border-radius: 18px !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
  background: rgba(255,240,248,0.06) !important;
  border: 1px solid rgba(255,182,217,0.2) !important;
  border-radius: 14px !important;
  padding: 0.5rem !important;
  text-align: center !important;
}
[data-testid="stMetricValue"] {
  color: var(--blush) !important;
  font-family: 'Quicksand', sans-serif !important;
  font-weight: 800 !important;
}
[data-testid="stMetricLabel"] {
  color: var(--text-muted) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
  background: rgba(255,240,248,0.06) !important;
  border: 1px solid rgba(255,182,217,0.2) !important;
  border-radius: 14px !important;
  color: var(--blush) !important;
  font-weight: 700 !important;
}

/* ── Divider ── */
hr {
  border: none !important;
  border-top: 1px solid rgba(255,182,217,0.15) !important;
  margin: 0.8rem 0 !important;
}

/* ── Success / Info / Warning / Error ── */
.stSuccess, .stInfo {
  background: rgba(255,240,248,0.08) !important;
  border: 1px solid rgba(255,182,217,0.3) !important;
  border-radius: 14px !important;
  color: var(--blush) !important;
}

/* ── Suggestion pills ── */
.suggestion-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(255,240,248,0.08);
  border: 1.5px solid rgba(255,182,217,0.3);
  border-radius: 999px;
  padding: 0.35rem 0.85rem;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--blush);
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(6px);
  font-family: 'Quicksand', sans-serif;
  letter-spacing: 0.01em;
}
.suggestion-pill:hover {
  background: rgba(255,95,162,0.15);
  border-color: rgba(255,95,162,0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(255,95,162,0.2);
  color: #FFC1DA;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }


/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(255,182,217,0.3);
  border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(255,95,162,0.5);
}

/* ── Spinner ── */
.stSpinner > div > div {
  border-top-color: #FF5FA2 !important;
}

/* ── Code blocks ── */
code {
  background: rgba(255,182,217,0.12) !important;
  border: 1px solid rgba(255,182,217,0.2) !important;
  border-radius: 8px !important;
  color: #FFB6D9 !important;
  font-size: 0.82rem !important;
}

pre {
  background: rgba(26,5,16,0.6) !important;
  border: 1px solid rgba(255,182,217,0.2) !important;
  border-radius: 14px !important;
}

/* ── Arabic text ── */
.arabic-line {
  direction: rtl;
  text-align: right;
  font-family: 'Tajawal', sans-serif;
  font-size: 1.02rem;
  font-weight: 500;
  line-height: 2.1;
  color: var(--text-soft);
  margin: 0.15rem 0;
}

/* ── Secret message ── */
.secret-msg {
  text-align: center;
  font-size: 0.7rem;
  color: rgba(255,182,217,0.4);
  font-style: italic;
  padding: 0.3rem;
  font-family: 'Quicksand', sans-serif;
  animation: floatAnim 3s ease-in-out infinite;
}

/* ── Cat typing indicator ── */
.cat-typing {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 0.3rem 0.7rem;
  background: rgba(255,182,217,0.1);
  border-radius: 999px;
  font-size: 0.75rem;
  color: var(--blush);
}

/* ── Glow button ── */
.glow-btn {
  box-shadow: 0 0 20px rgba(255,95,162,0.3), 0 0 40px rgba(255,95,162,0.1) !important;
}
</style>

<!-- Sakura petals -->
<div class="sakura-container">
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
  <div class="petal"></div>
</div>

<!-- Floating hearts -->
<div class="hearts-container">
  <div class="heart">💗</div>
  <div class="heart">🌸</div>
  <div class="heart">💕</div>
  <div class="heart">✨</div>
  <div class="heart">💗</div>
  <div class="heart">🌸</div>
  <div class="heart">💕</div>
  <div class="heart">💖</div>
</div>

<!-- Floating cats -->
<div class="cats-container">
  <div class="cat-float">🐱</div>
  <div class="cat-float">🐾</div>
  <div class="cat-float">🐱</div>
</div>
""", unsafe_allow_html=True)
