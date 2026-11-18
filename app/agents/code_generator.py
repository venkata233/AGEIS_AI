from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.state import AegisState
# Step 1: Define the generated code structure
class GeneratedFile(BaseModel):

    filename: str = Field(
        description="Name of the generated source file"
    )

    content: str = Field(
        description="Complete source code of the file"
    )


# Step 2: Define the complete code generation response
class CodeGenerationResult(BaseModel):

    files: list[GeneratedFile] = Field(
        description="List of generated application files"
    )
    # Step 3: Configure Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0
)


# Step 4: Enable structured output
structured_model = model.with_structured_output(
    CodeGenerationResult
)
# Step 5: Create the code generation prompt
code_generation_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a senior Python software engineer.

Your responsibility is to generate clean,
production-oriented application source code.

Use the provided software requirements
and architecture to generate the application.

Instructions:
1. Follow the provided architecture.
2. Use Python and FastAPI where specified.
3. Write complete, executable source code.
4. Follow clean coding practices.
5. Include appropriate error handling.
6. Use meaningful variable and function names.
7. Do not include explanations outside the source code.
8. Generate only the files requested.
"""),
    ("human", """
Requirements:
{requirements}

Architecture:
{architecture}

Generate the application source files.
""")
])
# Step 6: Connect prompt with Gemini
code_generation_chain = (
    code_generation_prompt | structured_model
)
# Step 7: Define the code generation agent
def code_generator_agent(state: AegisState):

    # Get requirements from AEGIS state
    requirements = state["requirement"]

    # Get architecture from AEGIS state
    architecture = state["architecture"]

    # Generate application code using Gemini
    result = code_generation_chain.invoke({
        "requirements": requirements,
        "architecture": str(architecture)
    })

    # Convert generated files into dictionaries
    generated_files = [
        file.model_dump()
        for file in result.files
    ]

    # Return generated code to LangGraph
    return {
        "code_files": generated_files,
        "status": "CODE_GENERATED"
    }