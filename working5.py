import requests
from transformers import BertTokenizer, BertModel
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

# Function to generate BERT embeddings
def generate_embeddings(tokens):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    
    # Encode the tokens
    encoded_inputs = tokenizer(tokens, return_tensors="pt", padding=True, truncation=True)
    
    # Generate embeddings
    with torch.no_grad():
        outputs = model(**encoded_inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)  # Average pooling
    
    return embeddings

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

# Example usage
if __name__ == "__main__":
    # Input sentence
    sentence = "he deposited money in the bank near the river bank"
    
    # Preprocess the sentence
    tokens = preprocess_text(sentence)
    print("Tokens after preprocessing:", tokens)
    
    # Generate embeddings for tokens
    embeddings = generate_embeddings(tokens)
    print("Generated BERT embeddings:", embeddings)
    
    # Define system and user prompts
    system_prompt = '''Categorize each word in the sentence based on its neighbors. 
    Choose the most specific category from: Finance, Legal, Numbers, Locations, Technical, 
    Action_and_Activity, Emotion, Time, People, Places, Objects, Food, Nature, Transportation, Household, 
    Event, Navigation, Sound, Animals, General.'''
    
    # Limit the number of tokens if necessary
    MAX_TOKENS = 50  # Set a maximum token length
    user_prompt = " ".join(tokens[:MAX_TOKENS])  # Truncate tokens if needed
    
    # Get the completion
    response = get_completion(system_prompt, user_prompt)
    
    # Print the response
    if response:
        print("API Response:")
        print(response)
