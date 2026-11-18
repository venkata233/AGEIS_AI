
from app.rag.ingestion import ingest_documents
from app.rag.vector_store import create_vector_store

# Step 1: Load documents and split into chunks
chunks = ingest_documents()

# Step 2: Store chunks and embeddings in ChromaDB
vector_store = create_vector_store(chunks)

# Step 3: Check stored records
stored_data = vector_store.get()

print("Total chunks:", len(chunks))
print("Stored vectors:", len(stored_data["ids"]))
print("Collection:", vector_store._collection.name)

print("\nChromaDB storage successful!")
