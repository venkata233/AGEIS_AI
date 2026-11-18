
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.state import AegisState


# Step 1: Locate the MCP server
SERVER_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "mcp"
    / "server.py"
)


# Step 2: Configure how to start the MCP server
server_params = StdioServerParameters(
    command=sys.executable,
    args=[str(SERVER_SCRIPT)]
)


# Step 3: Discover available MCP tools
async def discover_mcp_tools():

    async with stdio_client(server_params) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            tools_result = await session.list_tools()

            return [
                tool.name
                for tool in tools_result.tools
            ]


# Step 4: Save generated files using MCP
async def save_generated_files(code_files):

    execution_results = []
    generated_filenames = []

    async with stdio_client(server_params) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            for file in code_files:

                filename = file["filename"]
                content = file["content"]

                result = await session.call_tool(
                    "create_file",
                    arguments={
                        "filename": filename,
                        "content": content
                    }
                )

                if result.isError:
                    raise RuntimeError(
                        f"MCP failed to create {filename}"
                    )

                messages = [
                    item.text
                    for item in result.content
                    if hasattr(item, "text")
                ]

                generated_filenames.append(filename)
                execution_results.extend(messages)

    return generated_filenames, execution_results


# Step 5: Define the LangGraph MCP agent
def mcp_tools_agent(state: AegisState):

    # Discover available MCP tools
    available_tools = asyncio.run(
        discover_mcp_tools()
    )

    # Get generated code from LangGraph state
    code_files = state.get("code_files", [])

    if not code_files:
        raise ValueError(
            "No generated code files found in AEGIS state."
        )

    # Save generated files through MCP
    filenames, execution_results = asyncio.run(
        save_generated_files(code_files)
    )

    # Return updated LangGraph state
    return {
        "mcp_tools": available_tools,
        "generated_files": filenames,
        "mcp_execution_results": execution_results,
        "mcp_status": "MCP_FILES_SAVED",
        "status": "MCP_FILES_SAVED"
    }
