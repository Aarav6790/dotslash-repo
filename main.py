import nltk

def remove_stopwords(sentence):
    tokenizer = nltk.tokenize.RegexpTokenizer('[^\w\']+', gaps=True)
    text = sentence
    tokens = tokenizer.tokenize(text)
    tokens = [w for w in tokens if not w in nltk.corpus.stopwords.words('english')]
    return tokens