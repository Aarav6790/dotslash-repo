import requests
from transformers import BertTokenizer, BertModel
import torch
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Define the remove_stopwords function
def remove_stopwords(sentence):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(sentence)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return filtered_words

# Preprocessing function to clean and tokenize input
def preprocess_text(sentence):
    # Remove irrelevant characters
    cleaned_sentence = re.sub(r"[^\w\s]", "", sentence).lower()
    # Tokenize and remove stopwords
    tokens = remove_stopwords(cleaned_sentence)
    return tokens

# Function to call the API
def get_completion(system_prompt, user_prompt):
    # Define the API URL
    API_URL = "http://hackapi.rhosigma.tech/api/completion"
    # Define the API key
    API_KEY = "e54d4431-5dab-474e-b71a-0db1fcb9e659"
    
    # Define headers
    headers = {
        "X-API-Key": API_KEY,  # Pass the API key in the headers
        "Content-Type": "application/json"  # Set the content type to JSON
    }
    
    body = {
        "system": system_prompt,
        "user": user_prompt,
    }
    
    try:
        # Send the POST request
        response = requests.post(API_URL, headers=headers, json=body)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            return response.json()
        else:
            # Print error details if the request fails
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to process API response
def process_response(response):
    if "response" in response:
        # Split the response string into lines
        lines = response["response"].split("\n")
        # Remove empty lines and return as a list
        return [line.strip() for line in lines if line.strip()]
    else:
        print("No 'response' field in the API response.")
        return []

# Example usage
if __name__ == "__main__":
    # Input sentence
    sentence = input("Enter a sentence: ")
    
    # Preprocess the sentence
    tokens = preprocess_text(sentence)
    print("Tokens after preprocessing:", tokens)
    
    # Define system and user prompts
    system_prompt = '''Categorize each word in the sentence based on its neighbors. 
    Choose the most specific category from: Finance, Legal, Numbers, Locations, Technical, 
    Action_and_Activity, Emotion, Time, People, Places, Objects, Food, Nature, Transportation, Household, 
    Event, Navigation, Sound, Animals, General. output format=> word_category'''
    
    # Limit the number of tokens if necessary
    MAX_TOKENS = 50  # Set a maximum token length
    user_prompt = " ".join(tokens[:MAX_TOKENS])  # Truncate tokens if needed
    
    # Get the completion
    response = get_completion(system_prompt, user_prompt)
    
    # Process and print the response
    if response:
        processed_output = process_response(response)
        print("Processed Output as List:", processed_output)
