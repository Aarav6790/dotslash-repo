import subprocess
import requests
import json

# API configuration
API_URL = "http://hackapi.rhosigma.tech/api/completion"
API_KEY = "e54d4431-5dab-474e-b71a-0db1fcb9e659"

def run_first_py():
    """
    Execute first.py and capture its output.
    """
    try:
        # Run the first.py script and capture its output
        result = subprocess.run(
            ["python", "first.py"],
            capture_output=True,
            text=True,
            check=True
        )
        # Extract the filtered sentence from the output
        for line in result.stdout.splitlines():
            if line.startswith("Filtered Sentence:"):
                filtered_sentence = line.replace("Filtered Sentence:", "").strip()
                return json.loads(filtered_sentence.replace("'", '"'))  # Convert to list
    except subprocess.CalledProcessError as e:
        print(f"Error running first.py: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def send_to_api(words):
    """
    Send the filtered words to the API and append context tags.
    """
    # Create a user prompt by joining the words
    user_prompt = " ".join(words)
    
    # Define headers
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Define the system and user prompts
    system_prompt = (
        "Append context tags to each word in the input sentence. "
        "Do not process the sentence further, just append the tags."
    )
    
    body = {
        "system": system_prompt,
        "user": user_prompt
    }
    
    try:
        # Send the POST request
        response = requests.post(API_URL, headers=headers, json=body)
        
        if response.status_code == 200:
            api_response = response.json()
            return api_response.get("response", "No response")
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Step 1: Get filtered words from first.py
    filtered_words = run_first_py()
    
    if filtered_words:
        print("Filtered Words:", filtered_words)
        
        # Step 2: Send filtered words to the API
        api_response = send_to_api(filtered_words)
        
        # Step 3: Print the API response
        print("API Response:", api_response)
    else:
        print("No filtered words available.")
