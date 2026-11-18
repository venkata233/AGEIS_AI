
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from app.rag.retriever import search_knowledge


# Step 1: Configure Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0
)


# Step 2: Create RAG prompt
rag_prompt = ChatPromptTemplate.from_template("""
You are AEGIS, an AI software engineering assistant.

Answer the user's question using the provided context.

Context:
{context}

Question:
{question}

Instructions:
1. Use the provided context to answer.
2. Do not invent technical information.
3. If the answer is not available in the context, say:
   "I don't have enough information in my knowledge base."
4. Provide a clear and concise explanation.
""")


# Step 3: Connect the prompt with Gemini
rag_chain = rag_prompt | model


# Step 4: Generate an answer using RAG
def generate_answer(question: str):

    # Retrieve relevant documents
    results = search_knowledge(question)

    # Extract document content
    context = "\n\n".join(
        document.page_content
        for document, score in results
    )

    # Send context and question to Gemini
    response = rag_chain.invoke({
        "context": context,
        "question": question
    })

    # Step 5: Extract only readable answer text
    if isinstance(response.content, str):
        return response.content

    if isinstance(response.content, list):
        text_parts = [
            block["text"]
            for block in response.content
            if isinstance(block, dict)
            and block.get("type") == "text"
            and "text" in block
        ]

        return "\n".join(text_parts)

    return str(response.content)
