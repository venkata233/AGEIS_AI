from app.agents.mcp_tools import mcp_tools_agent


# Prepare sample LangGraph state
test_state = {
    "requirement": "Build a URL Shortener application"
}


# Execute MCP tools agent
result = mcp_tools_agent(test_state)


# Display results
print("MCP Agent Result:")
print(result)