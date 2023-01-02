from collections import namedtuple
import math

DATA_FILE = '05/data/glove.6B.300d.txt'
NAME = 'dittmar' # yannik isn't available, so I chose my surname

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

# Find the n nearest words to the given word using cosine similarity
def find_nearest(requestedWord, n=5):
    global data
    
    print(f"Finding nearest {n} words to {requestedWord.word}...")
    nearest = []
    worst = None
    for word in data:
        if word.word == requestedWord.word:
            continue

        sim = cosine_similarity(requestedWord.vector, word.vector)
        # Only add the word if it's one of the current n nearest
        if len(nearest) < n:
            nearest.append((word, sim))
            if worst is None or sim < worst[1]:
                worst = (word, sim)
        elif sim > worst[1]:
            nearest.remove(worst)
            nearest.append((word, sim))
            worst = min(nearest, key=lambda x: x[1])
        else:
            continue
        # Print the current nearest words
        print('\x1b[2K', [n[0].word for n in nearest], end="\r")
    print()
    print("Done.")
    nearest.sort(key=lambda x: x[1], reverse=True)
    return nearest

def main():
    global data
    load_data()

    # Get the requested word
    requestedWord = None
    for word in data:
        if word.word == NAME:
            requestedWord = word
            break
    
    if requestedWord is None:
        print("Word not found")
        return
    nearest = find_nearest(requestedWord)
    print("Nearest words and their similarities:")
    for word, sim in nearest:
        print(f"{word.word}: {sim}")

if __name__ == '__main__':
    main()