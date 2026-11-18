from app.rag.rag_chain import generate_answer

# Step 1: Ask a question
question = "What is AWS EKS?"

# Step 2: Generate an answer using RAG
answer = generate_answer(question)

# Step 3: Display the answer
print("\nAEGIS Answer:")
print(answer)