
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables from .env
load_dotenv()

# Configure Gemini embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


# Convert document chunks into embeddings
def generate_embeddings(chunks):

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    vectors = embedding_model.embed_documents(texts)

    return vectors
