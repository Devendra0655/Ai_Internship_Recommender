def get_career_advice(skills, missing_skills):
    prompt = f"""
    My current skills are: {', '.join(skills)}.
    Missing skills are: {', '.join(missing_skills)}.
    Suggest suitable internship roles and learning advice.
    """

    response = client.models.generate_content(
        model="models/gemini-1.0-pro",
        contents=prompt
    )

    return response.text
