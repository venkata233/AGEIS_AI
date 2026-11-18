# AEGIS — Agentic AI Software Engineering Platform

AEGIS is an MVP agentic engineering workflow that analyzes a software requirement,
plans engineering tasks, creates an architecture, and validates the result.

## Current workflow

Requirement → Requirement Agent → Planner → Architecture Agent → Validator

## Run locally

1. Create a virtual environment:
   python -m venv .venv

2. Activate it.

3. Install dependencies:
   pip install -r requirements.txt

4. Copy `.env.example` to `.env` and add your API key.

5. Start the API:
   uvicorn app.main:app --reload

6. Open:
   http://127.0.0.1:8000/docs

## Test request

POST `/engineer`

{
  "requirement": "Build a scalable URL shortener service with APIs, persistence, and analytics."
}

## Next phases

- Implementation Agent
- Actual FastAPI URL-shortener application
- PostgreSQL
- Redis
- Analytics worker
- Test Agent
- SRE Agent
- Security Agent
- Validation/rework loop
- Human approval
- Docker Compose
- Prometheus/Grafana/OpenTelemetry
- Brownfield repository analysis
