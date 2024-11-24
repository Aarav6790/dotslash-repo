import requests

def process_api_response(api_response):
    """
    Process the raw response text from the API and format it into a list of words with tags.
    """
    try:
        # Extract the 'response' field from the raw API response
        if api_response.startswith("{") and "response" in api_response:
            start_idx = api_response.index('"response":"') + len('"response":"')
            end_idx = api_response.rindex('"')
            response_content = api_response[start_idx:end_idx]
        else:
            print("Invalid API response format.")
            return []

        # Split the response into lines and format the output
        lines = response_content.split("\n")
        formatted_output = []
        for line in lines:
            if line.strip():  # Ignore empty lines
                parts = line.split(":")  # Split at ":" to separate the word and its tag
                if len(parts) == 2:
                    word = parts[0].strip()
                    tag = parts[1].strip().lower()  # Convert tag to lowercase
                    formatted_output.append(f"{word.lower()}_{tag}")

        return formatted_output

    except Exception as e:
        print("Error processing API response:", e)
        return []

def send_request_to_api(user_input):
    url = "http://hackapi.rhosigma.tech/api/completion"
    headers = {
        "X-API-Key": "e54d4431-5dab-474e-b71a-0db1fcb9e659",
        "Content-Type": "application/json",
    }
    body = {
        "system": "Process the sentence and return contextual tags for the words.",
        "user": user_input,
    }

    try:
        # Send POST request
        response = requests.post(url, headers=headers, json=body)

        # Get the raw response text
        print("Full API Response:", response.text)

        # Process the response and return the formatted output
        return process_api_response(response.text)

    except requests.RequestException as e:
        print("An error occurred while sending the request:", e)
        return []

def main():
    print("Welcome to the ISL Contextual Word Tagger!")
    print("Type a sentence to analyze, or type 'exit' to quit.")

    while True:
        user_input = input("\nEnter a sentence: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        contextual_tags = send_request_to_api(user_input)
        print("Contextual Tags:", contextual_tags)

if __name__ == "__main__":
    main()
