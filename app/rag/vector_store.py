
from pathlib import Path

from langchain_chroma import Chroma

from app.rag.embeddings import embedding_model


# Step 1: Define vector database location
VECTOR_STORE_DIR = (
    Path(__file__).resolve().parents[2] / "chroma_db"
)


# Step 2: Create vector database
def create_vector_store(chunks):

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(VECTOR_STORE_DIR),
        collection_name="aegis_knowledge"
    )

    return vector_store
