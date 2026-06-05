from flask import Flask, render_template, request
import os
import json
import random
import joblib
import pdfplumber

required_skills = [
    "python",
    "sql",
    "pandas",
    "numpy",
    "machine learning",
    "statistics",
    "power bi",
    "tableau",
    "excel",
    "data visualization"
]
app = Flask(__name__)

with open("intents.json", "r") as file:
    data = json.load(file)

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    response = ""
    user_message = ""
    found_skills = []
    missing_skills = []
    score = 0
    recommendations = []
    roadmap = []

    if request.method == "POST":
        print("Form submitted!")

        user_input = request.form["message"]
        resume_file = request.files.get("resume")

        if resume_file and resume_file.filename:

            save_path = os.path.join("uploads", resume_file.filename)

            resume_file.save(save_path)

            print("Resume saved:", save_path)
            text = ""

        with pdfplumber.open(save_path) as pdf:

           for page in pdf.pages:

             page_text = page.extract_text()

             if page_text:
                 text += page_text.lower()

        print(text[:300])
        for skill in required_skills:

            if skill in text:
              found_skills.append(skill)

            else:
              missing_skills.append(skill)

        score = (len(found_skills) / len(required_skills)) * 100
        if score < 40:

            roadmap = [
                "Learn Python Fundamentals",
                "Learn SQL Basics",
                "Practice Pandas and NumPy"
            ]

        elif score < 70:

            roadmap = [
                "Learn Machine Learning",
                "Build 2 Machine Learning Projects",
                "Practice Statistics"
            ]

        else:

            roadmap = [
                "Build Advanced Projects",
                "Learn Deployment",
                "Prepare for Data Science Interviews"
            ]

        
        if "machine learning" in missing_skills:
              recommendations.append(
                   "Learn Machine Learning and build a Customer Churn Prediction project"
            )

        if "statistics" in missing_skills:
             recommendations.append(
                    "Learn Statistics and practice probability concepts"
            )

        if "power bi" in missing_skills:
             recommendations.append(
                 "Learn Power BI and build a Sales Dashboard"
            )

        if "tableau" in missing_skills:
            recommendations.append(
               "Learn Tableau and create interactive dashboards"
            )

        if "sql" in missing_skills:
             recommendations.append(
                "Practice advanced SQL queries"
            )
        user_message = user_input

        user_vector = vectorizer.transform([user_input])

        predicted_tag = model.predict(user_vector)[0]

        for intent in data["intents"]:

            if intent["tag"] == predicted_tag:

                response = random.choice(intent["responses"])
                break

    return render_template(
    "index.html",
    response=response,
    user_message=user_message,
    found_skills=found_skills,
    missing_skills=missing_skills,
    score=score,
    recommendations=recommendations,
    roadmap=roadmap
    )
    
   
if __name__ == "__main__":
    app.run(debug=True)