import requests

# Define the API URL
API_URL = "http://hackapi.rhosigma.tech/api/completion"

# Define the API key
API_KEY = "e54d4431-5dab-474e-b71a-0db1fcb9e659"

# Function to call the API
def get_completion(system_prompt, user_prompt):
    # Define headers
    headers = {
        "X-API-Key": API_KEY,  # Pass the API key in the headers
        "Content-Type": "application/json"  # Set the content type to JSON
    }
    
    # Define the body
    body = {
        "system": system_prompt,
        "user": user_prompt
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
    # Define system and user prompts
    system_prompt = "You are a language model assisting with context-based word identification."
    user_prompt = "I deposited money in the bank."
    
    # Get the completion
    response = get_completion(system_prompt, user_prompt)
    
    # Print the response
    if response:
        print("API Response:")
        print(response)
