from app.rag.retriever import search_knowledge

results = search_knowledge(
    "What AWS service manages Kubernetes clusters?"
)

for document, score in results:

    print("\nScore:", score)

    print("Content:", document.page_content)

    print("Metadata:", document.metadata)