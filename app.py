from resume_utils import extract_skills
from flask import Flask, render_template, request, send_file
from recommender import recommend
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "internship.csv")


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    skills = []
    results = []

    if request.method == "POST":

        # Manual skills
        manual_skills = request.form.get("skills")
        if manual_skills:
            skills.extend([s.strip().lower() for s in manual_skills.split(",")])

        # Resume upload
        resume = request.files.get("resume")
        if resume and resume.filename.endswith(".pdf"):
            resume_skills = extract_skills(resume)
            skills.extend(resume_skills)

        skills = list(set(skills))

        # Filters
        filters = {
            "domain": request.form.get("domain"),
            "duration": request.form.get("duration"),
            "location": request.form.get("location")
        }

        results = recommend(skills, DATASET_PATH, filters)

    return render_template("index.html", skills=skills, results=results)


@app.route("/download-report")
def download_report():
    return send_file("reports/resume_report.txt", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
