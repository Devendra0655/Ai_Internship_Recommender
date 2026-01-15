from PyPDF2 import PdfReader

SKILLS_DB = [
    "python", "java", "sql", "machine learning", "deep learning",
    "data science", "html", "css", "javascript",
    "flask", "django", "pandas", "numpy"
]

def extract_skills(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text().lower()

    extracted_skills = [skill for skill in SKILLS_DB if skill in text]

    return extracted_skills
