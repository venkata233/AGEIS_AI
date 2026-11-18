
from app.rag.ingestion import ingest_documents
from app.rag.embeddings import generate_embeddings

# Load and split documents
chunks = ingest_documents()

# Generate embeddings
vectors = generate_embeddings(chunks)

# Display results
print("Total chunks:", len(chunks))
print("Total embeddings:", len(vectors))

if vectors:
    print("Vector dimensions:", len(vectors[0]))
    print("First 5 vector values:", vectors[0][:5])
