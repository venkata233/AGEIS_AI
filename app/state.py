from typing import TypedDict, List, Dict, Any

class AegisState(TypedDict, total=False):
    requirement: str
    requirement_analysis: Dict[str, Any]
    ambiguities: List[str]
    assumptions: List[str]
    tasks: List[Dict[str, Any]]
    architecture: Dict[str, Any]
    validation: Dict[str, Any]
    status: str
    knowledge_context: str
    knowledge_sources: List[str]
    mcp_tools: List[str]
    generated_files: List[str]
    mcp_execution_results: List[str]
    code_files: List[Dict[str, Any]]
    mcp_status: str