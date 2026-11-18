
from dotenv import load_dotenv

# Step 1: Load Gemini API key
load_dotenv()

from app.agents.code_generator import code_generator_agent


# Step 2: Prepare sample AEGIS state
test_state = {
    "requirement": """
    Build a URL Shortener application using Python and FastAPI.

    Users should be able to:
    1. Shorten long URLs.
    2. Redirect short URLs to original destinations.
    3. Store URL records in PostgreSQL.
    4. Use Redis for caching.
    5. Expose REST API endpoints.
    """,

    "architecture": {
        "application": "URL Shortener",
        "backend": "Python FastAPI",
        "database": "PostgreSQL",
        "cache": "Redis",
        "api": "REST API"
    }
}


# Step 3: Execute code generation agent
print("\nSending request to Gemini...")
print("Please wait while Gemini generates the application code.\n")

result = code_generator_agent(test_state)


# Step 4: Display code generation status
print("=" * 60)
print("CODE GENERATION STATUS:")
print(result["status"])
print("=" * 60)


# Step 5: Display generated files
print("\nGENERATED FILES:")

for file in result["code_files"]:

    print("\nFilename:", file["filename"])

    print("\nGenerated Code:")
    print("-" * 60)

    print(file["content"])

    print("\n" + "=" * 60)


# Step 6: Display total generated files
print(
    "\nTotal files generated:",
    len(result["code_files"])
)
