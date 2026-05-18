from chunking_01 import chunk_by_section
from embeddings_02 import generate_embedding
from vectordb_03 import VectorIndex
from bm25 import BM25Index


with open("./report.md", "r") as f:
    text = f.read()

# 1. Chunk the text by section
chunks = chunk_by_section(text)

# Semantic Search
## 2. Generate embeddings for each chunk
embeddings = generate_embedding(chunks)

## 3. Create a vector store and add each embedding to it
store = VectorIndex()
for embedding, chunk in zip(embeddings, chunks):
    store.add_vector(embedding, {"content": chunk})

## 4. Some time later, a user will ask a question. Generate an embedding for it
user_embedding = generate_embedding("What did the software engineering dept do last year?")

## 5. Search the store with the embedding, find the 2 most relevant chunks
results = store.search(user_embedding, 2)

print ("---------------RESULT Semantic Search---------------")
for doc, distance in results:
    print(distance, "\n", doc["content"][0:200], "\n")







