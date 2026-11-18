
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Step 1: Define the knowledge base directory
KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parents[1] / "knowledge_base"


# Step 2: Create the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


# Step 3: Load engineering documents
def load_documents():

    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.rglob("*"):

        if file_path.suffix.lower() not in [".txt", ".md"]:
            continue

        content = file_path.read_text(encoding="utf-8")

        document = Document(
            page_content=content,
            metadata={
                "source": str(file_path),
                "category": file_path.parent.name
            }
        )

        documents.append(document)

    return documents


# Step 4: Split documents into chunks
def split_documents(documents):

    chunks = text_splitter.split_documents(documents)

    return chunks


# Step 5: Complete ingestion workflow
def ingest_documents():

    documents = load_documents()

    chunks = split_documents(documents)

    return chunks
