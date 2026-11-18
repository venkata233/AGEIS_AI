from app.state import AegisState

def validator_agent(state: AegisState):
    requirements = state.get("requirement_analysis", {})
    architecture = state.get("architecture", {})

    checks = {
        "requirements_analyzed": bool(requirements),
        "architecture_created": bool(architecture),
        "api_defined": "api" in architecture,
        "database_defined": "database" in architecture,
        "cache_defined": "cache" in architecture,
        "analytics_defined": "analytics" in architecture,
        "observability_defined": "observability" in architecture
    }

    passed = sum(checks.values())
    total = len(checks)
    score = round((passed / total) * 100)
    status = "PASS" if score >= 90 else "REWORK_REQUIRED"

    return {
        "validation": {"score": score, "status": status, "checks": checks},
        "status": status
    }
