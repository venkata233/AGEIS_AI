from app.rag.retriever import search_knowledge
from app.state import AegisState

def knowledge_agent(state: AegisState):

    # Step 1: Get the user's requirement
    requirement = state["requirement"]

    # Step 2: Search the knowledge base
    results = search_knowledge(requirement)

    # Step 3: Extract document content
    knowledge_context = "\n\n".join(
        document.page_content
        for document, score in results
    )

    # Step 4: Extract document sources
    knowledge_sources = [
        document.metadata.get("source", "Unknown")
        for document, score in results
    ]

    # Step 5: Return information to LangGraph
    return {
        "knowledge_context": knowledge_context,
        "knowledge_sources": knowledge_sources,
        "status": "KNOWLEDGE_RETRIEVED"
    }