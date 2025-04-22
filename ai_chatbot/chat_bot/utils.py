import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.environ.get("API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 6000,
    "response_mime_type": "text/plain",
}

file_path = "./data/data.txt"
with open(file_path, "r") as file:
    file_contents = file.read()

system_instruction = (
    f"For your reference, these are the only products being sold in this app: {file_contents} only."
    "You are a helpful, friendly, and factual chatbot support assistant for a rice-selling e-commerce app in the Philippines. "
    "Your job is to guide customers in choosing the most suitable rice variety based on their preferences such as taste, texture, dietary needs, and budget. "
    "You also provide information about the benefits and downsides of each rice type. "
    "Only respond to questions directly related to Philippine rice varieties, rice preferences, cooking tips, storage, or rice-related health information. "
    "Do not answer questions that are unrelated to rice or e-commerce support. "
    "If the question is outside the scope of rice-related support, politely remind the user that you are only trained to help with rice inquiries. "
    "Always be polite, clear, and concise. Use Filipino rice varieties as examples such as Dinorado, Sinandomeng, Jasmine, Brown Rice, Black Rice, and Red Rice where relevant."
)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction=system_instruction,
)

def ask_gemini(user_input: str):
    response = model.generate_content(contents=user_input)

    # print(response.text)
    return response.text
