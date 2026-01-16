from resume_utils import extract_skills
from flask import Flask, render_template, request, send_file, jsonify
from recommender import recommend
from gemini_utils import get_career_advice, get_skill_gap_analysis
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "internship.csv")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    skills = []
    results = []
    career_advice = None

    if request.method == "POST":

        manual_skills = request.form.get("skills")
        if manual_skills:
            skills.extend([s.strip().lower() for s in manual_skills.split(",")])


        resume = request.files.get("resume")
        if resume and resume.filename.endswith(".pdf"):
            resume_skills = extract_skills(resume)
            skills.extend(resume_skills)

        skills = list(set(skills))


        filters = {
            "domain": request.form.get("domain"),
            "duration": request.form.get("duration"),
            "location": request.form.get("location")
        }

        results = recommend(skills, DATASET_PATH, filters)


        if results:
            all_required_skills = set()
            for result in results:
                # Assuming each result has a 'required_skills' field
                if 'required_skills' in result:
                    all_required_skills.update(result['required_skills'])

            missing_skills = list(all_required_skills - set(skills))


            career_advice = get_career_advice(skills, missing_skills)

    return render_template("index.html",
                           skills=skills,
                           results=results,
                           career_advice=career_advice)


@app.route("/api/career-advice", methods=["POST"])
def api_career_advice():

    data = request.get_json()
    skills = data.get("skills", [])
    missing_skills = data.get("missing_skills", [])

    advice = get_career_advice(skills, missing_skills)

    return jsonify({
        "success": True,
        "advice": advice
    })


@app.route("/api/skill-gap/<int:internship_id>", methods=["POST"])
def api_skill_gap(internship_id):

    data = request.get_json()
    user_skills = data.get("user_skills", [])
    required_skills = data.get("required_skills", [])

    analysis = get_skill_gap_analysis(user_skills, required_skills)

    return jsonify({
        "success": True,
        "analysis": analysis,
        "internship_id": internship_id
    })


@app.route("/download-report")
def download_report():
    return send_file("reports/resume_report.txt", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)