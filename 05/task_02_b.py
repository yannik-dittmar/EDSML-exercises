from collections import namedtuple
import math

DATA_FILE = '05/data/glove.6B.300d.txt'
SENTENCES = [
    "The quick brown fox jumps over the lazy dog",
    "George Armstrong Custer was a United States Army officer and cavalry commander in the American Civil War and the American Indian Wars",
    "Frederick Douglass was an American social reformer, abolitionist, orator, writer, and statesman",
]

WordItem = namedtuple("Word", "word vector")
Vector = namedtuple("Vector", "values length")
data = []

def vector_length(vector):
    return math.sqrt(sum([x * x for x in vector]))

def load_data():
    global data
    
    print("Loading data...")
    data = []
    with open(DATA_FILE, 'r', encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            word = str(parts[0])
            vector = [float(x) for x in parts[1:]]
            data.append(WordItem(word, Vector(vector, vector_length(vector))))
    print("Done.")

def cosine_similarity(a: Vector, b: Vector):
    product = [0] * len(a.values)
    
    for i in range(len(a.values)):
        product[i] = a.values[i] * b.values[i]

    return sum(product) / (a.length * b.length)

def tokenize(sentence):
    sentence = sentence.lower()
    sentence = sentence.replace(".", "").replace(",", "").replace("?", "").replace("!", "").replace(";", "").replace(":", "")
    return sentence.split()

def find_vectors(sentences):
    global data
    # Replace words with word vectors
    for word in data:
        for sentence in sentences:
            while word.word in sentence:
                sentence[sentence.index(word.word)] = word
    
    # Remove words that weren't found in data
    for sentence in sentences:
        i = 0
        while i < len(sentence):
            word = sentence[i]
            if type(word) == str:
                sentence.pop(i)
                i -= 1
                print(f"Word '{word}' not found in data, removing from sentence...")
            i += 1
    return sentences

def calc_sentence_vector(sentence):
    # Calculate the word vector for a whole sentence
    vector = [0] * len(sentence[0].vector.values)
    for word in sentence:
        for i in range(len(vector)):
            vector[i] += word.vector.values[i]
    for i in range(len(vector)):
        vector[i] /= len(sentence)
    return Vector(vector, vector_length(vector))

def main():
    global data
    load_data()
    
    sentences = SENTENCES.copy()
    sentences = list(map(tokenize, sentences))
    sentences = find_vectors(sentences)
    sentences = list(map(calc_sentence_vector, sentences))

    print(f"Cosine similarity between sentences 1 and 2: {cosine_similarity(sentences[0], sentences[1])}")
    print(f"Cosine similarity between sentences 2 and 3: {cosine_similarity(sentences[1], sentences[2])}")

if __name__ == '__main__':
    main()