# Import required modules
import os  # For accessing environment variables
from dotenv import load_dotenv  # To load API keys from a .env file
import google.generativeai as genai  # Gemini API for generating AI responses
from ecommerce_app.models import Product  # Import the Product model from your Django app

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API using your API key from the environment
genai.configure(api_key=os.environ.get("API_KEY"))

# Set the configuration for how the AI should respond
generation_config = {
    "temperature": 1,  # Controls randomness: higher = more random
    "top_p": 0.95,     # Controls diversity via nucleus sampling
    "top_k": 64,       # Limits number of tokens to consider
    "max_output_tokens": 6000,  # Max length of response
    "response_mime_type": "text/plain",  # Format of the AI response
}

def build_system_instruction():
    # Fetch all product data from the database along with their account info
    products = Product.objects.select_related("account").all()
    product_descriptions = []

    # Create a text summary for each product including basic details
    for product in products:
        product_descriptions.append(
            f"Product ID: {product.id}, Name: {product.product_name}, Price: {product.product_price}, Origin: {product.product_origin}, Description: {product.product_description} "
            f"Account: {product.account.username if product.account else 'N/A'}"
        )

    # Join all product summaries into a single string with a separator
    product_data = " | ".join(product_descriptions)

    # Return the final system instruction for Gemini with all rules and context
    return (
        f"For your reference, these are the only products being sold in this app: {product_data}, use this as a reference information but do not disclose the product ID or any sensitive database data. When redirecting the user to the url link of the product, use this format: http://127.0.0.1:8000/productpage/replace_this_with_product_id "
        "You are a helpful, friendly, and factual chatbot support assistant for a rice-selling e-commerce app in the Philippines. "
        "Your job is to guide customers in choosing the most suitable rice variety based on their preferences such as taste, texture, dietary needs, and budget. "
        "You also provide information about the benefits and downsides of each rice type. "
        "Only respond to questions directly related to Philippine rice varieties, rice preferences, cooking tips, storage, or rice-related health information. "
        "Do not answer questions that are unrelated to rice or e-commerce support. "
        "If the question is outside the scope of rice-related support, politely remind the user that you are only trained to help with rice inquiries. "
        "Always be polite, clear, and concise. Use Filipino rice varieties as examples such as Dinorado, Sinandomeng, Jasmine, Brown Rice, Black Rice, and Red Rice where relevant."
    )

def ask_gemini(user_input: str):
    # Get the full system instruction to control AI behavior
    system_instruction = build_system_instruction()

    # Initialize Gemini model with the system instruction and config
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
        system_instruction=system_instruction,
    )

    # Send the user input to Gemini and get the response
    response = model.generate_content(contents=user_input)
    
    # Return the response text
    return response.text
