import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("API_KEY"))

def ask_gemini(user_input):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=str(user_input),
    )

    # print(response.text)
    return response.text
