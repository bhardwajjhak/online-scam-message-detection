import streamlit as st
import pickle
import re
import math
# ---------------------------
# FUNCTIONS
# ---------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ---------------------------
# LOAD MODEL FILES
# ---------------------------
model = pickle.load(open("trained_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
threshold = pickle.load(open("threshold.pkl", "rb"))

print("Model Loaded Successfully")

# ---------------------------
# INPUT SECTION
# ---------------------------
st.title("📩 Online Scam Message Detection System")

text = st.text_area("Enter Message")

# ---------------------------
# VECTORIZE + MODEL OUTPUT
# ---------------------------
def get_prediction(message):
    cleaned = clean_text(message)
    X = vectorizer.transform([cleaned])
    score = model.decision_function(X)[0]
    return score

# ---------------------------
# PREDICTION + CONFIDENCE
# ---------------------------
if st.button("Check Message"):

    if text.strip() == "":
        st.warning("Please enter a message")

    else:
        # CLEAN TEXT
        text_lower = text.lower()

        # GET MODEL SCORE
        score = get_prediction(text)

        # CONFIDENCE (clean format)
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))

        probability = sigmoid(score)
        confidence_percent =round(
    max(probability, 1 - probability) * 100,
    2
)
       
        # STRONG KEYWORDS (IMPROVED DETECTION)
        spam_keywords = [
            "win", "won", "winner", "prize", "lottery", "reward", "cash", "free money", "gift",
            "click", "click here", "open link", "visit link",
            "urgent", "immediately", "verify now", "act now",
            "bank", "account blocked", "otp", "kyc", "password",
            "congratulations", "selected", "offer", "claim now",
            "security alert", "suspended"
        ]

        keyword_match = any(word in text_lower for word in spam_keywords)

        
        # FINAL OUTPUT LOGIC
        # ---------------------------
        keywords = ["win", "urgent", "bank", "otp", "verify", "click", "offer", "free", "prize"]
        keyword_flag = any(word in text.lower() for word in keywords)

        if confidence_percent > 0.5 or keyword_flag:
           st.error(f"🚨 SPAM / SCAM MESSAGE DETECTED (Confidence: {confidence_percent}%)")
        else:
           st.success(f"✅ NOT SPAM MESSAGE (Confidence: {confidence_percent}%)")
