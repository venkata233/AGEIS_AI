
from app.rag.ingestion import ingest_documents

# Run document ingestion
chunks = ingest_documents()

# Display total number of chunks
print("Total chunks:", len(chunks))

# Display each chunk
for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print("Content:", chunk.page_content)
    print("Metadata:", chunk.metadata)
