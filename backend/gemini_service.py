import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)


def generate_ai_requirements(title: str, domain: str, features: str):

    prompt = f"""
Create a detailed Business Requirement Document (BRD).

Title: {title}
Domain: {domain}
Features: {features}

Include:
1. Overview
2. Functional Requirements
3. Non-Functional Requirements
4. Use Cases
5. Constraints
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",   # ✅ IMPORTANT FIX
        contents=prompt
    )

    return response.text