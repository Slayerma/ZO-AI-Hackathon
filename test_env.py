import openai
import gradio as gr
import json
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load JSON data
def load_json_data(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

# Initialize messages list
messages = [{"role": "system", "content": "You are a helpful concierge"}]

# Chatbot function
def chatbot(user_input: str) -> str:
    global messages
    # Update the messages list with the user input
    messages.append({"role": "user", "content": user_input})

    # Generate a response from the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the response text
    ChatGPT_reply = response.choices[0].message.content

    # Append the assistant's response to the messages list
    messages.append({"role": "assistant", "content": ChatGPT_reply})

    return ChatGPT_reply

# Create Gradio interface
def CustomChatGPT(user_input):
    # Update the messages list with the user input
    messages.append({"role": "user", "content": user_input})

    # Create an OpenAI client instance
    client = openai.Client()

    # Generate a response from the OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the response text
    ChatGPT_reply = response.choices[0].message.content

    # Append the assistant's response to the messages list
    messages.append({"role": "assistant", "content": ChatGPT_reply})

    return ChatGPT_reply

# Gradio interface
demo = gr.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Hotel Service")
demo.launch(share = True)
