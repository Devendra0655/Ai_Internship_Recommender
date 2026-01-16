from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Generate content using gemini-2.5-flash (best model available)
response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents="Say hello in one sentence"
)

print(response.text)