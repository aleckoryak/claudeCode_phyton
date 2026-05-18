from chunking_01 import chunk_by_section
from embeddings_02 import generate_embedding
from vectordb_03 import VectorIndex
from bm25 import BM25Index


with open("./report.md", "r") as f:
    text = f.read()

# 1. Chunk the text by section
chunks = chunk_by_section(text)

#lexical search
## 2. Create a BM25 store and add documents
store = BM25Index()
for chunk in chunks:
    store.add_document({"content": chunk})

## 3. Search the store
results = store.search("What happened with INC-2023-Q4-011?", 3)

print ("---------------RESULT lexical Search---------------")
for doc, distance in results:
    print(distance, "\n", doc["content"][:200], "\n----\n")




