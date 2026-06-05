import pdfplumber

# Skills we want to check
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

# Read resume
with pdfplumber.open("resume.pdf") as pdf:

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text.lower()

# Find skills
found_skills = []
missing_skills = []

for skill in required_skills:

    if skill in text:
        found_skills.append(skill)

    else:
        missing_skills.append(skill)

print("\nSkills Found:")

for skill in found_skills:
    print("✓", skill)

print("\nMissing Skills:")

for skill in missing_skills:
    print("✗", skill)

print("\nRecommendations:")

if "machine learning" in missing_skills:
    print("→ Learn Machine Learning")
    print("→ Build a Customer Churn Prediction project")

if "statistics" in missing_skills:
    print("→ Learn Statistics")
    print("→ Practice hypothesis testing and probability")

if "power bi" in missing_skills:
    print("→ Learn Power BI")
    print("→ Build a Sales Dashboard project")

if "tableau" in missing_skills:
    print("→ Learn Tableau")
    print("→ Create interactive visualizations")

if "sql" in missing_skills:
    print("→ Practice SQL queries daily")

if "python" in missing_skills:
    print("→ Focus on Python fundamentals and data analysis")

total_skills = len(required_skills)

found_count = len(found_skills)

score = (found_count / total_skills) * 100

print(f"\nResume Score: {score:.2f}%")