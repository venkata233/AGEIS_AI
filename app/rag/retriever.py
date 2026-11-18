from langchain_chroma import Chroma

from app.rag.vector_store import VECTOR_STORE_DIR
from app.rag.embeddings import embedding_model

def get_vector_store():

    vector_store = Chroma(
        collection_name="aegis_knowledge",
        embedding_function=embedding_model,
        persist_directory=str(VECTOR_STORE_DIR)
    )

    return vector_store

def search_knowledge(query: str, k: int = 3):

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )

    return results