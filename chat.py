

import os
import openai
import gradio

# Set the API key as an environment variable
os.environ["OPENAI_API_KEY"] = "sk-proj-qDO5TVLSFy1l6CFSt70XT3BlbkFJq73zn3bw1MrPPk7dkOlo"

# Set up the conversation context
messages = [{"role": "system", "content": "You are a helpful concierge"}]

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
demo = gradio.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Hotel Service")
demo.launch(share = True)