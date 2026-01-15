import re

SKILL_KEYWORDS = [
    "python", "java", "c++", "sql", "machine learning",
    "data science", "deep learning", "flask", "django",
    "html", "css", "javascript", "react", "node",
    "cloud", "aws", "azure", "gcp", "docker",
    "tensorflow", "pandas", "numpy", "power bi", "tableau"
]

def extract_skills(text):
    text = text.lower()
    found_skills = set()

    for skill in SKILL_KEYWORDS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    return list(found_skills)
