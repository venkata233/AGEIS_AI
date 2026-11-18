import asyncio

from app.agents.mcp_tools import execute_mcp_tool


result = asyncio.run(
    execute_mcp_tool(
        "read_file",
        {
            "filename": "aegis_generated.py"
        }
    )
)

print("MCP Read Result:")

for item in result.content:
    if hasattr(item, "text"):
        print(item.text)