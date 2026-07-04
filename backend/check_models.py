import os
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=api_key)

try:
    # List all available models
    models = client.models.list()

    print("\n✅ Available Gemini Models:\n")

    for m in models:
        print(" -", m.name)

except Exception as e:
    print("\n❌ Error while fetching models:\n")
    print(e)