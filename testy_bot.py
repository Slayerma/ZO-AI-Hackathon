
import os
 
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
print(os.getenv('OPENAI_API_KEY')) # Debug: Print the API key to ensure it's loaded

import openai
import gradio as gr
import json
from dotenv import load_dotenv, find_dotenv

# Load environment variables

openai.api_key = os.getenv("OPENAI_API_KEY")

# Load JSON data
def load_json_data(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

import openai
import gradio as gr
import json
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load JSON data
def load_json_data(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

# Load necessary data
faq_data = load_json_data('faqs.json')
property_info = load_json_data('property_info.json')
guest_preferences = load_json_data('guest_preferences.json')

# Chatbot function
def chatbot(user_input: str) -> str:
    # Placeholder for check-in process
    if "check-in" in user_input.lower():
        return "Check-in process initiated. Please provide your details."
    
    # Placeholder for personalized recommendations
    if "recommendations" in user_input.lower():
        return "Generating personalized recommendations based on your preferences."
    
    # Existing functionality for property info, guest preferences, and FAQs
    if "property info" in user_input.lower():
        # If the user is asking for information about the property, return the
        # property information as a single string.
        if 'property_info' not in globals():
            raise ValueError("property_info is not loaded.")
        return "\n".join(f"{key.title()}: {value}" for key, value in property_info.items())

    # Check if the user is asking for information about the guest preferences
    elif "guest preferences" in user_input.lower():
        # If the user is asking for information about the guest preferences, return
        # the guest preferences as a single string.
        if 'guest_preferences' not in globals():
            raise ValueError("guest_preferences is not loaded.")
        return "\n".join(
            f"{preference['id']}: {preference['data'][0]['text']}"
            for preference in guest_preferences
            if preference is not None and "data" in preference and preference["data"] is not None
        )

    # Check if the user is asking for information about the FAQs
    elif "faq" in user_input.lower():
        # If the user is asking for information about the FAQs, return the FAQs as
        # a single string.
        if 'faq_data' not in globals():
            raise ValueError("faq_data is not loaded.")
        return "\n\n".join(
            f"Q: {faq['question']}\nA: {faq['answer']}"
            for faq in faq_data
            if faq is not None and "question" in faq and "answer" in faq
        )

    # If none of the above conditions are met, use the OpenAI API to generate a response
    else:
        # Prepare the prompt for the OpenAI API
        prompt = f"User Input: {user_input}\n\nAssistant:"

        # Call the OpenAI API
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
                return_prompt=False,
            )
        except Exception as e:
            raise e

        # Get the response from the API
        try:
            assistant_response = response.choices[0].text.strip()
        except (AttributeError, IndexError):
            raise ValueError("response or response.choices[0] is None")

        return assistant_response
    # ... (existing code from the second snippet)

# Create Gradio interface
import gradio as gr

# Create Gradio interface
def create_chatbot_interface() -> None:
    """
    Create and launch the Gradio interface for the chatbot.
    """
    # Load JSON data
    try:
        faq_data = load_json_data('faqs.json')
        property_info = load_json_data('property_info.json')
        guest_preferences = load_json_data('guest_preferences.json')
        knowledge_base = load_json_data('knowledge_base.json')
    except TypeError as e:
        raise ValueError("Failed to load JSON data. Please ensure data files are present and properly formatted.") from e

    # Set up OpenAI API key
    api_key: str = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    openai.api_key = api_key

    # Create the Gradio interface
    iface: gr.Interface = gr.Interface()
    iface = gr.Interface(
        fn=chatbot,
        inputs=gr.inputs.Textbox(lines=7, placeholder="Enter your message here..."),
        outputs="text",
        title="Zo World Chatbot Assistant",
        description="Ask me anything related to your stay at Zo World!",
        theme="huggingface"
    )
    iface.launch()

if __name__ == "__main__":
    create_chatbot_interface()

