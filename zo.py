# Import required libraries
import os
import openai

import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
openai.api_key = os.environ.get("sk-proj-qDO5TVLSFy1l6CFSt70XT3BlbkFJq73zn3bw1MrPPk7dkOlo")

# Define functions
import os
import json

def preprocess_data(data: dict) -> dict:
    """Faster and more efficient preprocessing of data sources."""
    return {key: data.get(key) for key in ("property_info", "faqs", "guest_preferences", "knowledge_base")}

try:
    with open('property_info.json', 'r') as json_file:
        json_data = json.load(json_file)
except FileNotFoundError:
    print("Error: property_info.json file not found in the current directory.")
except ValueError:
    print("Error: Invalid JSON data in property_info.json.")
else:
    # Call functions with loaded data
    preprocessed_data = preprocess_data(json_data)
    if preprocessed_data is not None:
        # Call the extract_knowledge_base function
        knowledge_base = extract_knowledge_base(preprocessed_data)
        print(preprocessed_data)
        print(knowledge_base)

def extract_knowledge_base(preprocessed_data):
    """
    Extract a knowledge base from preprocessed data

    Args:
    preprocessed_data (dict): Preprocessed data structures (e.g., property_info, faqs, guest_preferences)

    Returns:
    dict: Knowledge base data structure
    """
    knowledge_base = {}
    for key in ('property_info', 'faqs', 'guest_preferences'):
        if key in preprocessed_data:
            knowledge_base[key] = preprocessed_data[key]
    return knowledge_base


# Load JSON data
try:
    with open('property_info.json', 'r') as json_file:
        json_data = json.load(json_file)
except FileNotFoundError:
    print("Error: property_info.json file not found in the current directory.")
except ValueError:
    print("Error: Invalid JSON data in property_info.json.")
else:
    # Call functions with loaded data
    preprocessed_data = preprocess_data(json_data)
    if preprocessed_data is not None:  # Add this check
        knowledge_base = extract_knowledge_base(preprocessed_data)
        print(preprocessed_data)
        print(knowledge_base)
def gpt_chat(
    user_input: str, conversation_history: List[str]
) -> str:
    """Interact with GPT-3.5-turbo model"""
    api_key = "sk-proj-qDO5TVLSFy1l6CFSt70XT3BlbkFJq73zn3bw1MrPPk7dkOlo"

    client = openai.Client(api_key)
    response = client.complete(
        engine="davinci-codex",
        prompt=user_input,
        max_tokens=15,
        stop=["==== EXIT ====="],
        context=conversation_history,
    )

    return response["choices"][0]["text"].strip()




# Example usage
user_input = "Hello, how can I help you?"
conversation_history = ["Previous chat history..."]
response = gpt_chat(user_input, conversation_history)
print(response)


def handle_check_in(user_input: str, conversation: List[str], guest_info: Optional[Dict[str, str]] = None) -> Tuple[str, Optional[Dict[str, str]]]:
    """Handle the check-in process for a guest."""
    if not user_input or not conversation:
        raise ValueError("User input and conversation are required")
    if guest_info is None:
        guest_info = {}

    name = next((x[1] for x in (x.split("check-in") for x in conversation) if len(x) > 1), None)
    response = f"Welcome, {name or 'there'}! Please provide your check-in details." if name else "I didn't understand your request. Please provide a check-in request with your name."
    updated_guest_info = {"name": name} if name else guest_info

    return response, updated_guest_info


def extract_name_from_check_in(message: str) -> Optional[str]:
    """Extract the name from a check-in message."""
    return message.split("check-in", 1)[1].strip() if "check-in" in message else None




def faq_response(query: str, faqs: dict) -> str:
    """Return answer to query if found in FAQs, else a generic message."""

    # Check for null pointer references
    if not query or not faqs:
        raise ValueError("Query and FAQs are required")

    # Look for matching FAQ (optimized for fewer comparisons)
    query_lower = query.lower()
    for question in faqs:
        if query_lower in question.lower():
            return faqs[question]

    # If no match found, return a default response
    return "I'm sorry, but I don't have any information on that topic."



# Example usage
user_input = "What is the check-in time?"
knowledge_base = {}  # You can populate this with actual FAQs
response = faq_response(user_input, knowledge_base)
print(response)

def generate_recommendations(preferences):
    """Generate personalized recommendations based on guest preferences."""
    location_map = {
        "city": ("museums", "art galleries"),
        "beach": ("surfing lessons",),
    }
    cuisine_map = {
        "Mexican": ("taco stands",),
        "Indian": ("spice markets",),
    }
    budget_map = {
        "luxury": ("private wine tastings",),
        "mid-range": ("brewery or distillery tours",),
    }

    recommendations = []
    for location, activities in location_map.items():
        if location == preferences["location"]:
            recommendations.extend(activities)
    for cuisine, activities in cuisine_map.items():
        if cuisine == preferences["cuisine"]:
            recommendations.extend(activities)
    for budget, activities in budget_map.items():
        if budget == preferences["budget"]:
            recommendations.extend(activities)

    return recommendations




def main():
    """Main function to run the chatbot"""

    # Load and preprocess data
    data = preprocess_data()
    kb = build_knowledge_base(data)

    # Load property info from JSON file
    try:
        with open("property_info.json") as f:
            property_info = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        property_info = {}

    # Chatbot loop
    while True:
        try:
            # Get user input and convert to lowercase
            user_input = input("You: ").lower()

            # Check for exit condition
            if user_input in ("quit", "exit", "bye"):
                break

            # Process user input and generate response
            guest_info, guest_preferences = None, None
            if "check-in" in user_input:
                response = check_in(user_input, guest_info)
            elif "recommendation" in user_input:
                guest_preferences = extract_guest_preferences(user_input)
                recommendations = recommendation_engine(guest_preferences)
                response = "".join(
                    [
                        "Here are some personalized recommendations for you: ",
                        ", ".join(recommendations),
                    ]
                )
            else:
                response = faq_response(user_input, kb) or gpt_chat(user_input)

            # Print chatbot's response
            print("Chatbot:", response)

        except Exception:
            pass





if __name__ == "__main__":
    main()
