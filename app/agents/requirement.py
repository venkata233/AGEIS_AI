#from langchain_openai import ChatOpenAI
#from langchain_core.prompts import ChatPromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from app.state import AegisState


class RequirementAnalysis(BaseModel):
    summary: str = Field(description="Short summary of the requirement")
    functional_requirements: list[str] = Field(
        description="Functional requirements"
    )
    non_functional_requirements: list[str] = Field(
        description="Non-functional requirements"
    )
    ambiguities: list[str] = Field(
        description="Missing or unclear requirements"
    )
    assumptions: list[str] = Field(
        description="Reasonable assumptions"
    )


model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0
)

structured_model = model.with_structured_output(RequirementAnalysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a senior software requirements engineer.
Analyze the user's software requirement.

Identify:
1. Functional requirements
2. Non-functional requirements
3. Ambiguities
4. Reasonable assumptions

Do not invent unnecessary requirements.
"""),
    ("human", "{requirement}")
])

chain = prompt | structured_model


def requirement_agent(state: AegisState):
    result = chain.invoke({
        "requirement": state["requirement"]
    })

    return {
        "requirement_analysis": result.model_dump(),
        "ambiguities": result.ambiguities,
        "assumptions": result.assumptions,
        "status": "REQUIREMENTS_ANALYZED"
    }
