
from pathlib import Path

from mcp.server.fastmcp import FastMCP


# Step 1: Initialize MCP server
mcp = FastMCP("AEGIS Filesystem Server")


# Step 2: Define the AEGIS workspace directory
WORKSPACE_DIR = (
    Path(__file__).resolve().parents[2]
    / "generated_projects"
    / "mcp_workspace"
).resolve()


# Step 3: Create workspace directory if it doesn't exist
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)


# Step 4: Validate file paths for security
def get_safe_path(filename: str) -> Path:

    file_path = (WORKSPACE_DIR / filename).resolve()

    # Prevent access outside the AEGIS workspace
    if not file_path.is_relative_to(WORKSPACE_DIR):
        raise ValueError(
            "Access denied: Path is outside AEGIS workspace"
        )

    return file_path


# Step 5: MCP Tool - Create a file
@mcp.tool()
def create_file(filename: str, content: str) -> str:
    """
    Create a file inside the AEGIS workspace.
    """

    file_path = get_safe_path(filename)

    # Create nested directories if required
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write content into the file
    file_path.write_text(content, encoding="utf-8")

    return f"File created successfully: {filename}"


# Step 6: MCP Tool - Read a file
@mcp.tool()
def read_file(filename: str) -> str:
    """
    Read a file from the AEGIS workspace.
    """

    file_path = get_safe_path(filename)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"File not found: {filename}"
        )

    # Read file content
    content = file_path.read_text(encoding="utf-8")

    return content


# Step 7: Start MCP server using standard input/output
if __name__ == "__main__":
    mcp.run(transport="stdio")
