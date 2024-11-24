import requests
import json
import time

API_URL = "http://hackapi.rhosigma.tech/api/completion"
API_KEY = "e54d4431-5dab-474e-b71a-0db1fcb9e659"

# Define a mapping for more simplified context tags
context_mapping = {
    "noun": "general",
    "verb": "action",
    "adjective": "description",
    "possessive noun": "general",
    "conjunction": "general",
    "preposition": "general",
    "adverb": "general",
    "part of the Earth's structure": "geography",
    "part of the body": "anatomy",
    "technology": "tech",
    "location": "geography",
    "human": "general",
    "place": "geography",
    "time": "general"
}

def process_sentence(sentence):
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    system_prompt = (
        "Analyze the sentence, identify the context of each word, append a relevant tag, "
        "and return the result as a JSON list."
    )

    payload = {"system": system_prompt, "user": sentence}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            # Ensure the response is a valid JSON
            try:
                result = response.json()  # This will parse the response as JSON
                print("Full API Response:", result)  # Debugging line
                api_response = result.get("response", [])

                if not api_response:
                    print("No words with context received.")
                    return []

                # Process the API response to create simplified context tags
                simplified_tags = []
                for word_info in api_response:
                    word = word_info.get("word", "").lower()
                    context = word_info.get("context", "").lower()

                    # Map the context to a simplified one-word tag
                    if context in context_mapping:
                        tag = f"{word}_{context_mapping[context]}"
                        simplified_tags.append(tag)

                return simplified_tags
            except json.JSONDecodeError:
                print("Error: Received a malformed JSON response from the API.")
                return "Error: Malformed response"
        elif response.status_code == 429:  # Rate limit exceeded
            print("Rate limit exceeded. Retrying after 10 seconds...")
            time.sleep(10)
            return process_sentence(sentence)
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    print("Welcome to the ISL Contextual Word Tagger!")
    print("Type a sentence to analyze, or type 'exit' to quit.\n")

    while True:
        user_input = input("Enter a sentence: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if len(user_input) == 0:
            print("Please enter a valid sentence.")
            continue

        # Process the input sentence
        contextual_tags = process_sentence(user_input)

        if contextual_tags == "Error: Malformed response":
            print("The API returned an invalid response. Please try again.")
        elif contextual_tags:
            print("Contextual Tags:", contextual_tags)
        else:
            print("No response received. Please try again.")
