import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Define categories with seed words
CATEGORIES = {
    "finance": ["money", "bank", "loan", "investment"],
    "legal": ["law", "court", "contract", "agreement"],
    "technical": ["technology", "computer", "software", "programming"]
,
    "everyday": ["food", "drink", "house", "school"],
    "numbers": ["value", "percentage", "quantity", "amount"],
    "states_and_cities": ["city", "state", "country", "location"],
}

def get_bert_embedding(word, sentence):
    """Get the BERT embedding for a word in a sentence."""
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        hidden_states = outputs.last_hidden_state  # Shape: (batch_size, seq_len, hidden_dim)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    try:
        word_index = tokens.index(word)
    except ValueError:
        return None
    return hidden_states[0, word_index, :].numpy()  # Shape: (hidden_dim,)

def classify_word(word, sentence, categories=CATEGORIES):
    """Classify a word into one of the predefined categories based on similarity."""
    word_embedding = get_bert_embedding(word, sentence)
    if word_embedding is None:
        return "unknown"
    
    max_similarity = -1
    best_category = "unknown"
    for category, seeds in categories.items():
        seed_embeddings = [get_bert_embedding(seed, " ".join(seeds)) for seed in seeds]
        seed_embeddings = [emb for emb in seed_embeddings if emb is not None]
        if not seed_embeddings:
            continue
        avg_seed_embedding = np.mean(seed_embeddings, axis=0)  # Average seed embeddings
        similarity = cosine_similarity([word_embedding], [avg_seed_embedding])[0, 0]
        if similarity > max_similarity:
            max_similarity = similarity
            best_category = category
    return best_category

def classify_sentence(sentence):
    """Classify all words in a sentence."""
    tokens = tokenizer.tokenize(sentence.lower())
    classifications = {}
    for token in tokens:
        category = classify_word(token, sentence)
        classifications[token] = category
    return classifications

# Example usage
if __name__ == "__main__":
    sentence = "He deposited money in the bank for his car he bought in Chandigarh."
    classifications = classify_sentence(sentence)
    print("Word Classifications:")
    for word, category in classifications.items():
        print(f"{word}: {category}")
