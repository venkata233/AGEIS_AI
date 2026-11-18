""" from app.state import AegisState

def planner_agent(state: AegisState):
    tasks = [
        {"id": "ARCH-001", "name": "Design system architecture", "depends_on": []},
        {"id": "API-001", "name": "Define REST API", "depends_on": ["ARCH-001"]},
        {"id": "DB-001", "name": "Design database schema", "depends_on": ["ARCH-001"]},
        {"id": "CODE-001", "name": "Implement URL shortener", "depends_on": ["API-001", "DB-001"]},
        {"id": "TEST-001", "name": "Generate automated tests", "depends_on": ["CODE-001"]},
        {"id": "SRE-001", "name": "Define SLOs and observability", "depends_on": ["ARCH-001"]},
        {"id": "SEC-001", "name": "Perform security validation", "depends_on": ["CODE-001"]},
        {"id": "VAL-001", "name": "Validate engineering solution",
         "depends_on": ["TEST-001", "SRE-001", "SEC-001"]}
    ]
    return {"tasks": tasks, "status": "PLAN_CREATED"}  """



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.state import AegisState


# Step 1: Define individual task structure
class EngineeringTask(BaseModel):
    id: str = Field(description="Unique task identifier")
    name: str = Field(description="Short task name")
    description: str = Field(description="Detailed task description")
    depends_on: list[str] = Field(
        description="IDs of prerequisite tasks"
    )


# Step 2: Define complete engineering plan
class EngineeringPlan(BaseModel):
    tasks: list[EngineeringTask] = Field(
        description="Engineering tasks in execution order"
    )


# Step 3: Configure Gemini
model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0
)

structured_model = model.with_structured_output(EngineeringPlan)


# Step 4: Create planner prompt with RAG knowledge
planner_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a senior software engineering project planner.

Use the user's requirement and the retrieved engineering
knowledge to create a detailed implementation plan.

Engineering Knowledge:
{knowledge_context}

Instructions:
1. Identify all necessary engineering tasks.
2. Generate unique task IDs.
3. Provide a clear task name.
4. Provide a detailed task description.
5. Identify task dependencies.
6. Arrange tasks in logical execution order.
7. Do not generate unnecessary tasks.
8. Include testing and security validation.
9. Use the engineering knowledge when relevant.
10. Do not invent information that is not supported
    by the requirement or engineering knowledge.
"""),
    ("human", "{requirement}")
])


# Step 5: Connect prompt and Gemini
planner_chain = planner_prompt | structured_model


# Step 6: Define planner agent
def planner_agent(state: AegisState):

    # Get requirement and retrieved knowledge
    requirement = state["requirement"]
    knowledge_context = state.get("knowledge_context", "")

    # Generate engineering plan using Gemini
    result = planner_chain.invoke({
        "requirement": requirement,
        "knowledge_context": knowledge_context
    })

    # Return generated tasks to LangGraph
    return {
        "tasks": [task.model_dump() for task in result.tasks],
        "status": "PLAN_CREATED"
    }
