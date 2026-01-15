from google import genai
import os

# Load API key from environment variable
API_KEY = os.getenv("GIVE_API_KEY")

client = genai.Client(api_key=API_KEY)

def get_career_advice(user_skills, missing_skills):
    prompt = f"""
    User has the following skills:
    {', '.join(user_skills)}

    The following skills are missing for better internship matches:
    {', '.join(missing_skills)}

    Provide:
    1. Career advice
    2. Skill improvement roadmap
    3. Suggested learning resources
    4. Motivation guidance
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text
