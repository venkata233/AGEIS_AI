from app.state import AegisState

def architecture_agent(state: AegisState):
    architecture = {
        "application": "URL Shortener",
        "api": {
            "technology": "FastAPI",
            "endpoints": [
                "POST /api/v1/urls",
                "GET /{short_code}",
                "GET /api/v1/urls/{id}/analytics"
            ]
        },
        "database": {
            "technology": "PostgreSQL",
            "purpose": "Persistent URL and analytics storage"
        },
        "cache": {
            "technology": "Redis",
            "purpose": "Fast URL lookup"
        },
        "analytics": {
            "technology": "Redis Streams",
            "pattern": "Asynchronous processing"
        },
        "observability": {
            "metrics": "Prometheus",
            "dashboard": "Grafana",
            "tracing": "OpenTelemetry"
        },
        "deployment": {
            "local": "Docker Compose",
            "production": "Kubernetes"
        }
    }
    return {"architecture": architecture, "status": "ARCHITECTURE_CREATED"}
