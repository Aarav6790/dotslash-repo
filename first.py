import spacy
from nltk.corpus import stopwords

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize stop words
import nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Function to remove stopwords
def remove_stopwords(sentence):
    words = sentence.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return filtered_words

# Sample sentence
sentence = "I deposited money in the bank. the boat is in the bank of the river."
filtered_sentence = remove_stopwords(sentence)
print("Filtered Sentence:", filtered_sentence)
