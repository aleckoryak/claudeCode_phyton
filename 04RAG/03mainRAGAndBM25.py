from chunking_01 import chunk_by_section
from embeddings_02 import generate_embedding
from vectordb_03 import VectorIndex
from bm25 import BM25Index
from retriever import Retriever


with open("./report.md", "r") as f:
    text = f.read()

# 1. Chunk the text by section
chunks = chunk_by_section(text)

# Create a vector index, a bm25 index, then use them to create a Retriever
vector_index = VectorIndex(embedding_fn=generate_embedding)
bm25_index = BM25Index()

retriever = Retriever(bm25_index, vector_index)

# Add all chunks to the retriever, which internally passes them along to both indexes
# Note: converted to a bulk operation to avoid rate limiting errors from VoyageAI
retriever.add_documents([{"content": chunk} for chunk in chunks])

## 3. Search the store
results = retriever.search("What happened with INC-2023-Q4-011?", 3)

print ("---------------RESULT retriever Search---------------")
for doc, distance in results:
    print(distance, "\n", doc["content"][:200], "\n----\n")