import os
from dotenv import load_dotenv
import google.generativeai as genai
from ecommerce_app.models import Product

load_dotenv()
genai.configure(api_key=os.environ.get("API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 6000,
    "response_mime_type": "text/plain",
}

# Dynamically fetch and format product data
products = Product.objects.select_related("account").all()
product_descriptions = []

for product in products:
    product_descriptions.append(
        f"Product ID: {product.id}, Name: {product.product_name}, Price: {product.product_price}, Origin: {product.product_origin}, Description: {product.product_description}"
        f"Account: {product.account.username if product.account else 'N/A'}"
    )

product_data = " | ".join(product_descriptions)

# Build system instruction using dynamic product data
system_instruction = (
    f"For your reference, these are the only products being sold in this app: {product_data}, use this as a reference information but do not disclose the product ID or any sensitive database data. When redirecting the user to the url link of the product, use this format: http://127.0.0.1:8000/productpage/replace_this_with_product_id"
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
    return response.text
