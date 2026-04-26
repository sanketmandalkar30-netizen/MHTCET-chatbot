import streamlit as st
from difflib import get_close_matches
import re
import random

# -------------------------------
# KNOWLEDGE BASE (EXPANDED)
# -------------------------------

faq_data = {
    "what is mht cet": "MHT-CET is a state-level entrance exam for Engineering, Pharmacy, and Agriculture courses in Maharashtra.",

    "eligibility": "You must have passed or appeared in Class 12 with PCM/PCB subjects.",

    "exam date": "MHT-CET is usually conducted between April and May.",

    "syllabus": "Based on Maharashtra State Board Class 11 & 12.",

    "marking scheme": "No negative marking. +1 or +2 per correct answer.",

    "cutoff": "Cutoff depends on college, branch, and difficulty level. Top colleges need 95-99 percentile.",

    "top colleges": "COEP, VJTI, SPIT, PICT are among top engineering colleges.",

    "hello": "Hello! 👋 Ask me anything about MHT-CET.",
    "hi": "Hi 😊 How can I help you?",
    "bye": "Good luck for your exam 🚀"
}

# -------------------------------
# SMART MATCHING
# -------------------------------

def get_best_match(user_input):
    questions = list(faq_data.keys())
    matches = get_close_matches(user_input, questions, n=1, cutoff=0.3)
    return matches[0] if matches else None

# -------------------------------
# MARKS → PERCENTILE LOGIC
# -------------------------------

def marks_to_percentile(marks):
    # Approximation logic (based on trends)
    if marks >= 160:
        return "99+ percentile 🔥 (Top colleges like COEP/VJTI possible)"
    elif marks >= 140:
        return "97-99 percentile"
    elif marks >= 120:
        return "95-97 percentile"
    elif marks >= 100:
        return "90-95 percentile"
    elif marks >= 80:
        return "80-90 percentile"
    else:
        return "Below 80 percentile"

# -------------------------------
# INTENT DETECTION (AI-LIKE)
# -------------------------------

def chatbot_response(user_input):
    text = user_input.lower()

    # -------------------------------
    # 1. MARKS DETECTION (SMART)
    # -------------------------------
    numbers = re.findall(r'\d+', text)

    if numbers:
        marks = int(numbers[0])

        if "marks" in text or "percentile" in text or "score" in text:
            result = marks_to_percentile(marks)
            return f"📊 Your estimated percentile for {marks} marks:\n\n👉 {result}"

    # -------------------------------
    # 2. CUTOFF INTELLIGENCE
    # -------------------------------
    if "cutoff" in text or "college" in text:
        return """🎯 MHT-CET Cutoff Insight:

- COEP / VJTI → 98-99 percentile
- SPIT / PICT → 95-98 percentile
- Good colleges → 85-95 percentile

Cutoff changes every year based on competition.
"""

    # -------------------------------
    # 3. FUZZY FAQ MATCH
    # -------------------------------
    best_match = get_best_match(text)

    if best_match:
        return faq_data[best_match]

    # -------------------------------
    # 4. SMART DEFAULT (AI FEEL)
    # -------------------------------
    smart_replies = [
        "Try asking about marks, cutoff, colleges, syllabus 😊",
        "I can help with marks vs percentile, colleges, exam info!",
        "Ask me something like '120 marks percentile' or 'cutoff for COEP'"
    ]

    return random.choice(smart_replies)

# -------------------------------
# STREAMLIT UI
# -------------------------------

st.set_page_config(page_title="MHT-CET AI Chatbot", page_icon="🎓")

st.title("🎓 MHT-CET AI Helpdesk Chatbot")
st.write("Ask about cutoff, marks, percentile, colleges, etc.")

# Session memory
if "history" not in st.session_state:
    st.session_state.history = []

# Input
user_input = st.text_input("You:", placeholder="e.g. 120 marks percentile")

# Send button
if st.button("Send"):
    if user_input.strip():
        response = chatbot_response(user_input)

        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", response))

# Display chat
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**🧑 {sender}:** {message}")
    else:
        st.markdown(f"**🤖 {sender}:** {message}")