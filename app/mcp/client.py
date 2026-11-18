
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Step 1: Locate the MCP server
SERVER_SCRIPT = (
    Path(__file__).resolve().parent / "server.py"
)


# Step 2: Configure how to start the MCP server
server_params = StdioServerParameters(
    command=sys.executable,
    args=[str(SERVER_SCRIPT)]
)


# Step 3: Define the MCP client workflow
async def main():

    # Start the server and establish communication
    async with stdio_client(server_params) as (read_stream, write_stream):

        # Create an MCP client session
        async with ClientSession(read_stream, write_stream) as session:

            # Initialize the connection
            await session.initialize()

            print("\nConnected to AEGIS MCP Server!")

            # Step 4: Discover available tools
            tools_result = await session.list_tools()

            print("\nAvailable MCP Tools:")

            for tool in tools_result.tools:
                print("-", tool.name)

            # Step 5: Create a file using MCP
            create_result = await session.call_tool(
                "create_file",
                arguments={
                    "filename": "client_test.py",
                    "content": 'print("Hello from AEGIS MCP Client!")'
                }
            )

            print("\nCreate File Result:")
            print(create_result.content)

            # Step 6: Read the file using MCP
            read_result = await session.call_tool(
                "read_file",
                arguments={
                    "filename": "client_test.py"
                }
            )

            print("\nRead File Result:")

            for item in read_result.content:
                if hasattr(item, "text"):
                    print(item.text)


# Step 7: Run the asynchronous client
if __name__ == "__main__":
    asyncio.run(main())
