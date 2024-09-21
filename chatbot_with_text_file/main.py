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
# Function to load allowed words from a text file
def load_allowed_words(filename):
    with open(filename, 'r') as file:
        allowed_words = set(file.read().lower().split())  # Convert to lowercase and split into words
    return allowed_words

# Function to load chatbot responses from a JSON file
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def ignore_prepositions(words):
    """Removes prepositions and articles from a list of words."""
    stop_words = {"the", "what", "my", "best", "i", "?", "should", "an", "a", "in", "of", "to", "for", "and", "nor", "but", "or", "yet", "is", "so", "if", "because", "as", "while", "since", "until", "after", "before", "during", "while", "since", "until", "after", "before", "during", "although", "though", "even", "if", "unless", "except", "excepting", "besides", "except", "but", "save", "save", "except", "is", "but", "save"}
    return [word.lower() for word in words if word.lower() not in stop_words]

# Function to validate user input against the allowed words
def is_valid_input(user_input, allowed_words):
    user_words = user_input.lower().split()  # Convert user input to lowercase and split into words
    words_in_input_filtered = ignore_prepositions(user_words)
    #allowed_words1=allowed_words.lower().split()
    return all(word in allowed_words for word in words_in_input_filtered)  # Check if all words are allowed

# Function to get a response from JSON file based on intents
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

# Main chatbot function
def chatbot():
    count=0
    # Load allowed words from text file
    allowed_words = load_allowed_words('allowed_words.txt')  # Text file with valid words

    # Load chatbot responses from JSON file
      # JSON file with predefined responses

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
        x=["hi", "hello", "hey"]
        for i in range(len(x)):
            
            if user_input.lower()==x[i]:
                print("Chatbot:Hello! How can I help you today?")
                
                
    
    # Check for questions about the assistant's identity
        y=["who are you", "what are you"]
        for i in range(len(y)):
            if user_input.lower()==y[i].lower():
                print("Chatbot:I'm an AI assistant here to help you with your queries about our products and services. How can I assist you?")
        
        z=["Goodbye", "Bye"]
        for j in range(len(z)):
            if user_input.lower()==z[j].lower():
                print("Chatbot:Goodbye! Have a great day!")
        m=["Goodbye", "Bye", "who are you", "what are you", "hi", "hello", "hey" ]
        for l in range(len(m)):
            if user_input.lower()!=m[l].lower():
                count=count+1
        if count>0:
                if is_valid_input(user_input, allowed_words):
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
