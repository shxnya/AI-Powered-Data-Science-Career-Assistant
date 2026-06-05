import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
with open("intents.json", "r") as file:
    data = json.load(file)

patterns = []
tags = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern)
        tags.append(intent["tag"])

# Train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

model = LogisticRegression()
model.fit(X, tags)

# Chat loop
while True:

    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    user_vector = vectorizer.transform([user_input])

    probabilities = model.predict_proba(user_vector)[0]

    confidence = max(probabilities) * 100

    predicted_tag = model.predict(user_vector)[0]
    if confidence < 20:
          print("Bot: Sorry, I don't understand that question yet.")
          print(f"Confidence: {confidence:.2f}%")
          continue

    for intent in data["intents"]:
        if intent["tag"] == predicted_tag:
            response = random.choice(intent["responses"])
            print("Bot:", response)
            print(f"Confidence: {confidence:.2f}%")
            break