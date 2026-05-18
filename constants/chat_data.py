"""
constants/chat_data.py — App constants, modes, moods, prompts for SemSemty AI
"""
import datetime
import os

APP_NAME    = "SemSemty AI"
APP_SLOGAN  = "Your Pink Radiology Bestie 🩻🐾"
APP_VERSION = "2.0.0"

# ── Groq API ─────────────────────────────────────────────────────
# NOTE: GROQ_API_KEY is read at call-time in llm_service.py via os.getenv()
# Do NOT cache it here — dotenv may not be loaded yet at import time
GROQ_MODEL    = "llama-3.3-70b-versatile"
MAX_TOKENS    = 1400
TEMPERATURE   = 0.72

MODES = [
    "🩻 Radiology Q&A",
    "🔬 X-Ray Analyzer",
    "📚 Study PDF",
    "✨ Cute Notes",
    "📖 Study Buddy",
    "💕 Pink Talk",
]

MOODS = ["😊 Happy", "😴 Sleepy", "📚 Study Mode", "💖 Need Love"]

MOOD_PROMPTS = {
    "😊 Happy":       "Sama is happy and energetic! Match her energy — be bright, bubbly, and enthusiastic 🌸",
    "😴 Sleepy":      "Sama is tired and sleepy. Be extra gentle, short, and very encouraging. Give her virtual hugs 💕",
    "📚 Study Mode":  "Sama is in full study mode! Be focused, structured, and give her the best radiology knowledge 🩻",
    "💖 Need Love":   "Sama needs extra emotional support right now. Be warm, loving, and remind her how incredible she is 💗",
}

LOVE_MESSAGES = [
    "💗 Mohamed loves your smile more than anything",
    "🌸 You are his favorite person in the whole world",
    "🐾 Stay strong, future radiology queen 👑",
    "💕 Someone is always so proud of you",
    "✨ You make life softer and more beautiful",
    "💗 You are the cutest future radiologist 🩻",
    "🌸 Mohamed will always choose you, every single time",
    "🐱 Even your mistakes are adorable to him 💕",
    "✨ You're doing better than you think, Semsem 💗",
    "💖 He's proud of you every single day",
    "🌸 You are his whole world wrapped in pink 💕",
    "🩻 The best diagnosis? Having you in his life 💗",
]

REMINDERS = [
    "💧 Semsem! Drink water right now 🌸",
    "👀 Look away from the screen — your eyes need rest 💕",
    "🍎 Eat something, future radiology queen 💗",
    "🤸 Stand up and stretch, Sama 🌸",
    "😴 Don't forget to sleep — beauty rest is important too ✨",
    "Mohamed is proud of you 💗",
    "🌸 You're doing amazingly well, Semsem 🐾",
    "☕ Take a small break — you've been studying so hard!",
    "🎵 Play your favourite song as a reward 💕",
    "💗 You are going to be the most wonderful radiologist 🩻",
]

QUICK_PROMPTS = {
    "🩻 Radiology Q&A": [
        ("🫀 Chest X-Ray",         "Explain how to systematically read a chest X-ray step by step — approach, zones, findings."),
        ("🧠 Brain CT",            "Explain how to read a brain CT scan — windows, structures, common pathologies."),
        ("🦴 Bone X-Ray",          "How do I read bone X-rays? Explain density, cortex, trabecular pattern, and common fractures."),
        ("📡 MRI Basics",          "Explain MRI basics for radiology students: T1, T2, FLAIR, DWI sequences and what they show."),
        ("🩸 Contrast Studies",    "Explain the use of contrast in radiology: types, indications, contraindications, reactions."),
        ("📝 5 MCQ Practice",      "Give me 5 radiology MCQs with 4 options each, correct answer, and full explanation."),
    ],
    "🔬 X-Ray Analyzer": [
        ("📋 Full Analysis",       "Please analyze this image and describe all findings in detail."),
        ("🫁 Lung Fields",         "Focus on the lung fields in this image — describe any abnormalities."),
        ("🫀 Cardiac Silhouette",  "Analyze the cardiac silhouette and mediastinum in this image."),
        ("🦴 Bone & Joints",       "Examine the bony structures and joints in this image."),
        ("⚠️ Spot the Finding",    "What is the key abnormal finding in this image? Give differential diagnoses."),
        ("📊 Teaching Points",     "Give me 3 teaching points a radiology student should learn from this image."),
    ],
    "📚 Study PDF": [
        ("📋 Summarize File",      "Summarize the uploaded file with clear headings and key bullet points."),
        ("🎯 Make Flashcards",     "Create flashcards from the uploaded content in Q: ... / A: ... format."),
        ("❓ MCQ Practice",        "Generate 5 MCQs from the uploaded file with A–D options, correct answer, and explanation."),
        ("🧠 Explain Hard Parts",  "What is the most difficult concept in this file? Explain it simply with an analogy."),
        ("🔑 Top 10 Points",       "What are the 10 most important points I must remember from this file?"),
        ("📊 Mind Map",            "Create a structured mind map outline of the main topics in this file."),
    ],
    "✨ Cute Notes": [
        ("📝 Organize My Notes",   "Help me organize my radiology notes in a clear, beautiful format with sections and bullet points."),
        ("🗂️ Create Study Sheet",  "Create a one-page quick reference study sheet for the topic I describe."),
        ("🔑 Key Mnemonics",       "Give me the best mnemonics for radiology that every radiology student must know."),
        ("📊 Comparison Table",    "Create a comparison table for radiological findings in different conditions."),
        ("✏️ Rewrite Simply",      "Take my notes and rewrite them in a simpler, easier to understand way."),
        ("🌸 Pretty Format",       "Reformat my notes with beautiful headers, bullets, and emojis to make studying fun."),
    ],
    "📖 Study Buddy": [
        ("📅 Study Plan Today",    "Create a detailed study plan for today — with subjects, breaks, and goals."),
        ("⏰ Pomodoro Session",    "Start a Pomodoro study session with me — 25 min focus, 5 min break! Let's go 🔥"),
        ("🧠 Memory Techniques",  "What are the best memorisation techniques for radiology students? Give me examples."),
        ("💪 Motivate Me!",       "I really need motivation to study right now — pump me up! 🔥💗"),
        ("📊 Exam Strategy",      "I have an exam soon. Help me build an efficient revision strategy for radiology."),
        ("🌟 Active Recall",      "Explain active recall and spaced repetition and how to use them for radiology."),
    ],
    "💕 Pink Talk": [
        ("💬 How Are You?",       "Hey SemSemty! How are you today? 🌸💕"),
        ("✨ Fun Radiology Fact", "Tell me a fascinating radiology or medical imaging fact most people don't know!"),
        ("🎀 Surprise Me",        "Surprise me with something cute, interesting, or sweet today ✨"),
        ("🩻 Career Advice",      "Give me advice and motivation for my journey as a future radiologist 💗"),
        ("💌 Open When Tired",    "I'm really tired right now and need a warm message 💕"),
        ("🌸 Tell Me Something",  "Tell me something beautiful to brighten my day 🌸"),
    ],
}

MODE_META = {
    "🩻 Radiology Q&A": {
        "icon": "🩻", "color": "#FF66A3",
        "desc": "X-Ray, CT, MRI, anatomy, pathology, MCQs, and everything radiology 💗",
    },
    "🔬 X-Ray Analyzer": {
        "icon": "🔬", "color": "#FF9EC7",
        "desc": "Upload an X-ray or scan image → AI radiology analysis with findings 🩻✨",
    },
    "📚 Study PDF": {
        "icon": "📚", "color": "#C9B8FF",
        "desc": "Upload a lecture PDF → summaries, flashcards & MCQ practice 🎀",
    },
    "✨ Cute Notes": {
        "icon": "✨", "color": "#FFB6D9",
        "desc": "Organize notes, create study sheets, mnemonics, and more 🌸",
    },
    "📖 Study Buddy": {
        "icon": "📖", "color": "#87CEEB",
        "desc": "Study plans, Pomodoro sessions, memory tips, motivation 💪",
    },
    "💕 Pink Talk": {
        "icon": "💕", "color": "#FF9EC7",
        "desc": "Talk to me about anything — I'm always here for you 🐾",
    },
}


def get_today_index() -> int:
    return datetime.date.today().toordinal()
