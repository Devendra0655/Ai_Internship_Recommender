import pandas as pd

# Domain-wise expected skills (logical mapping)
DOMAIN_SKILLS = {
    "data science": ["python", "pandas", "numpy", "machine learning", "sql"],
    "ai": ["python", "machine learning", "deep learning", "nlp"],
    "web development": ["html", "css", "javascript", "react"],
    "software": ["python", "java", "problem solving", "oops"],
    "marketing": ["seo", "content writing", "analytics"],
}

def recommend(user_skills, csv_path, filters):
    df = pd.read_csv(csv_path)
    results = []

    user_skills = [s.lower() for s in user_skills]

    for _, row in df.iterrows():

        # Infer domain from title (since dataset is limited)
        title = str(row["internship_title"]).lower()

        domain = "general"
        for d in DOMAIN_SKILLS:
            if d in title:
                domain = d
                break

        expected_skills = DOMAIN_SKILLS.get(domain, [])

        matched = list(set(user_skills) & set(expected_skills))
        missing = list(set(expected_skills) - set(user_skills))

        score = 0
        if expected_skills:
            score = int((len(matched) / len(expected_skills)) * 100)

        # Apply filters safely
        if filters.get("location"):
            if filters["location"].lower() not in str(row["location"]).lower():
                continue

        if filters.get("duration"):
            if filters["duration"] not in str(row["duration"]):
                continue

        results.append({
            "title": row["internship_title"],
            "company": row["company_name"],
            "location": row["location"],
            "duration": row["duration"],
            "stipend": row["stipend"],
            "domain": domain.title(),
            "matched_skills": matched,
            "missing_skills": missing,
            "score": score
        })

    # Sort by best match
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results
