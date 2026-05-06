import json
import re
import collections
import nltk
import unicodedata

chunks_json = json.load(open("data/chunks.json", "r", encoding="utf-8"))

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")

stop_words = set(nltk.corpus.stopwords.words("english"))

allowed_single = {"x", "y", "z", "w", "b", "n", "m", "k", "t", "p", "q", "r", "i", "j"}

synonyms = {
    "backpropagation": ["back propagation", "back-propagation"],
    "gradient descent": ["gd"],
    "stochastic gradient descent": ["sgd"],
    "overfitting": ["over-fit", "over fit"],
    "dropout": ["drop out"],
    "convolutional neural network": ["cnn"],
    "recurrent neural network": ["rnn"],
    "long short term memory": ["lstm"],
    "transformer": ["transformers"],
    "batch normalization": ["batch norm"],
    "data augmentation": ["data aug"]
}

def preprocess_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    for synonym, variants in synonyms.items():
        for variant in variants:
            text = text.replace(variant, synonym)
    text = re.sub(r'[^\w\s]', ' ', text)


    tokens = nltk.word_tokenize(text)
    tokens = [token for token in tokens if token not in stop_words]
    
    tokens = [token for token in tokens if len(token) > 1 or token in allowed_single]

    return tokens

def score_chunk(query, query_tokens, chunk_tokens):
    query_counter = collections.Counter(query_tokens)
    chunk_counter = collections.Counter(chunk_tokens)
    score = 0
    for token in query_counter:
        if token in chunk_counter:
            score += chunk_counter[token] * query_counter[token]
    return score


def retrieve(query, chunk_texts, top_k=5):
    query_tokens = preprocess_text(query)
    scored_chunks = []
    for chunk in chunk_texts:
        chunk_tokens = preprocess_text(chunk["text"])
        score = score_chunk(query, query_tokens, chunk_tokens)
        if score > 0:
            scored_chunks.append((score, chunk))
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return scored_chunks[:top_k]

if __name__ == "__main__":
    query = "What is back propagation?"
    top_chunks = retrieve(query, chunks_json)
    for score, chunk in top_chunks:
        print(f"Score: {score}, Chapter: {chunk['chapter']}, Pages: {chunk['page_start']}-{chunk['page_end']}")
        print(f"Text: {chunk['text'][:200]}...\n")


    
