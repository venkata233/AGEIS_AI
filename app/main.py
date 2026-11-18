
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Step 1: Load environment variables
load_dotenv()

from app.graph import aegis_graph


# Step 2: Create FastAPI application
app = FastAPI(
    title="AEGIS",
    description="Agentic AI Software Engineering Platform",
    version="0.1.0"
)


# Step 3: Define request structure
class EngineeringRequest(BaseModel):
    requirement: str


# Step 4: Root endpoint
@app.get("/")
def root():
    return {
        "name": "AEGIS",
        "description": "Agentic AI Software Engineering Platform",
        "status": "running"
    }


# Step 5: Engineering endpoint
@app.post("/engineer")
def engineer(request: EngineeringRequest):

    # Prepare initial LangGraph state
    initial_state = {
        "requirement": request.requirement,
        "status": "STARTED"
    }

    # Execute complete AEGIS workflow
    result = aegis_graph.invoke(initial_state)

    # Return workflow results
    return {
        "status": result.get("status"),
        "mcp_status": result.get("mcp_status"),
        "requirement_analysis": result.get("requirement_analysis"),
        "knowledge_context": result.get("knowledge_context"),
        "knowledge_sources": result.get("knowledge_sources"),
        "mcp_tools": result.get("mcp_tools"),
        "generated_files": result.get("generated_files"),
        "mcp_execution_results": result.get("mcp_execution_results"),
        "tasks": result.get("tasks"),
        "architecture": result.get("architecture"),
        "code_files": result.get("code_files"),
        "validation": result.get("validation")
    }
