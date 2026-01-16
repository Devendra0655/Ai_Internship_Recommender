from google import genai
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def clean_and_format_output(text):


    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)


    text = re.sub(r'^(\d+)\.\s+(.+?):', r'<h3>\1. \2</h3>', text, flags=re.MULTILINE)


    lines = text.split('\n')
    formatted_lines = []
    in_list = False

    for line in lines:
        stripped = line.strip()


        if stripped.startswith('•') or stripped.startswith('-') or (
                len(line) > 0 and line[0] == ' ' and ':' in stripped):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True

            clean_line = re.sub(r'^[•\-\s]+', '', stripped)
            formatted_lines.append(f'<li>{clean_line}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            if stripped:
                formatted_lines.append(f'<p>{stripped}</p>')

    if in_list:
        formatted_lines.append('</ul>')

    result = '\n'.join(formatted_lines)


    result = re.sub(r'<p>(<h3>.*?</h3>)</p>', r'\1', result)


    result = re.sub(r'<p>\s*</p>', '', result)

    return result.strip()


def get_career_advice(skills, missing_skills):

    prompt = f"""
    Based on the following information, provide detailed career guidance:

    Current Skills: {', '.join(skills) if skills else 'None specified'}
    Missing Skills: {', '.join(missing_skills) if missing_skills else 'None identified'}

    Please provide a well-structured response with the following sections:

    1. Top 3-5 suitable internship roles based on current skills
    List each role with a brief description of how the current skills apply.

    2. Priority skills to learn from the missing skills list
    Identify the most important skills to focus on.

    3. A brief learning roadmap
    Provide 2-3 sentences per skill on how to approach learning it.

    4. Resources or platforms to learn these skills
    List specific platforms, courses, or documentation for each skill.

    Format your response with clear numbered sections and use bullet points for lists. Keep it concise and actionable.
    """

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        return clean_and_format_output(response.text)
    except Exception as e:
        return f"<p class='error'>Error generating career advice: {str(e)}</p>"


def get_skill_gap_analysis(user_skills, internship_requirements):

    prompt = f"""
    Analyze the skill gap between a candidate and an internship position:

    Candidate Skills: {', '.join(user_skills)}
    Required Skills: {', '.join(internship_requirements)}

    Provide a structured analysis with:

    1. Match percentage
    2. Skills the candidate has that match
    3. Critical missing skills
    4. Quick tips to bridge the gap

    Keep it brief, encouraging, and well-formatted with bullet points where appropriate.
    """

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        return clean_and_format_output(response.text)
    except Exception as e:
        return f"<p class='error'>Error analyzing skills: {str(e)}</p>"