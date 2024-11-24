import requests
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources
# nltk.download("stopwords")
# nltk.download("punkt")

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

# Function to classify tokens using a BERT-based classifier
def classify_tokens_with_bert(tokens):
    # Load pretrained BERT tokenizer and classifier model
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=20)

    # Define categories (for demonstration; update as per your needs)
    categories = ["Finance", "Legal", "Numbers", "Locations", "Technical",
                  "Action_and_Activity", "Emotion", "Time", "People", "Places",
                  "Objects", "Food", "Nature", "Transportation", "Household",
                  "Event", "Navigation", "Sound", "Animals", "General"]

    token_labels = []
    for token in tokens:
        # Encode each token
        inputs = tokenizer(token, return_tensors="pt", padding=True, truncation=True)
        
        # Get predictions
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=1)
            label = categories[predictions.item()]
            token_labels.append((token, label))

    return token_labels

# Function to call the GPT-4 API
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
    
    # Classify tokens using BERT-based classifier
    bert_classifications = classify_tokens_with_bert(tokens)
    print("BERT Classifications:", bert_classifications)
    
    # Prepare data for GPT-4 API
    combined_input = [
        f"{word} ({bert_label})" for word, bert_label in bert_classifications
    ]
    user_prompt = " ".join(combined_input)

    # Define system prompt
    system_prompt = '''
    Refine the categorization of each word based on its BERT-assigned category and its neighbours. 
Map each word to one of the following categories: 
Finance, Legal, Numbers, Locations, Technical, Action_and_Activity, Emotion, Time, People, Places, Objects, Food, Nature, Transportation, Household, Event, Navigation, Sound, Animals, General.
Format: word_finalCategory
    '''

    # Call the GPT-4 API
    response = get_completion(system_prompt, user_prompt)
    
    # Process and print the response
    if response:
        processed_output = process_response(response)
        print("Processed Output as List:", processed_output)
