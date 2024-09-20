import json
import random
import requests
import os
import google.generativeai as genai
import re


genai.configure(api_key="AIzaSyAFAhfsuTtZV8Lrke97RXF1OaSZ1BY9MvQ")

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    
)
# Function to load JSON data from file
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def ignore_prepositions(words):
    """Removes prepositions and articles from a list of words."""
    stop_words = {"the", "an", "a", "in", "of", "to", "for", "and", "nor", "but", "or", "yet", "so", "if", "because", "as", "while", "since", "until", "after", "before", "during", "while", "since", "until", "after", "before", "during", "although", "though", "even", "if", "unless", "except", "excepting", "besides", "except", "but", "save", "save", "except", "is", "but", "save"}
    return [word for word in words if word.lower() not in stop_words]

def check_words_in_json(user_input, json_data):
    words_in_input = re.findall(r'\w+', user_input.lower())  # Extract words from input
    
    # Collect all words from the JSON file examples
    words_in_json = set()
    for intent in json_data['intents']:
        for example in intent['examples']:
            words_in_json.update(example.lower().split())
    
    # Check if all input words are present in the JSON file
    words_in_input_filtered = ignore_prepositions(words_in_input)
    words_in_json_filtered = ignore_prepositions(words_in_json)
    if(words_in_input!=None):
        

        return any(word in words_in_json_filtered for word in words_in_input_filtered)

# Function to get response from local JSON intents
def get_local_response(user_input, intents_data):
    user_input = user_input.lower()

    # Iterate through the intents in the JSON file
    for intent in intents_data['intents']:
        # Check if the user input matches any example from the intent
        for example in intent['examples']:
            if user_input == example.lower():
                # Return a random response from the list of possible responses
                return random.choice(intent['responses'])
    
    # If no match is found in the local data, return None
    return None

# Function to get response from an external chatbot API (like OpenAI or Gemini)


# Main function to interact with the chatbot
def chatbot():
    # Load the chatbot data from the JSON file
    chatbot_data = load_json('data.json')
    
    # Get the API key from environment variable (or hard-code it)
    api_key = "AIzaSyCg2X5t4aL7yrIazZcGMLfrB_2MGsC4YjA"
    
    if not api_key:
        print("Error: API Key not found. Please set the API key.")
        return
    
    print("Chatbot: Hi! Ask me anything.")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        
        if check_words_in_json(user_input, chatbot_data):
        # Get the chatbot's response
            response = get_local_response(user_input, chatbot_data)
            
            if response is None:
            # If no match is found in the JSON, use the external chatbot API
                r = chat.send_message(user_input)
                response=r.text
            print(f"Chatbot: {response}")

        else:
            print("I can't answer your question")
        
       

       

# Start the chatbot
if __name__ == '__main__':
    chatbot()
