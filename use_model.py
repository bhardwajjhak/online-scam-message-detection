import pickle
import re
import numpy as np

# -----------------------------
# 1. CLEAN FUNCTION
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -----------------------------
# 2. LOAD MODEL FILES
# -----------------------------
model = pickle.load(open("trained_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
threshold = pickle.load(open("threshold.pkl", "rb"))

print("Model Loaded Successfully")

# -----------------------------
# 3. INPUT
# -----------------------------
text = input("Enter message: ")

text_clean = clean_text(text)

# -----------------------------
# 4. VECTORIZE
# -----------------------------
X = vectorizer.transform([text_clean])

# -----------------------------
# 5. MODEL OUTPUT (ONLY SCORE USED INTERNALLY)
# -----------------------------
score = model.decision_function(X)[0]

# -----------------------------
# 6. PREDICTION
# -----------------------------
prediction = 1 if score > threshold else 0

# -----------------------------
# 7. CONFIDENCE SCORE (ONLY OUTPUT WE KEEP)
# -----------------------------
confidence_score = 1 / (1 + np.exp(-score))  # sigmoid → 0 to 1

# -----------------------------
# 8. FINAL OUTPUT
# -----------------------------
print("\n----------------------")

if prediction == 1:
    print("🚨 SPAM MESSAGE")
else:
    print("✅ NOT SPAM")

print("Confidence Score:", round(confidence_score, 4))