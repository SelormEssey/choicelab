"""ChoiceLab API.

The API is intentionally small during the research foundation phase.
It exposes project metadata only and contains no recommendations, account data,
or decision logic.
"""

from fastapi import FastAPI
from pydantic import BaseModel


class ProjectStatus(BaseModel):
    name: str
    phase: str
    message: str


app = FastAPI(
    title="ChoiceLab API",
    version="0.1.0",
    description="Research foundation API for ChoiceLab.",
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return a lightweight liveness response for local development."""
    return {"status": "ok"}


@app.get("/v1/project-status", response_model=ProjectStatus, tags=["project"])
def project_status() -> ProjectStatus:
    """Return non-sensitive public project metadata."""
    return ProjectStatus(
        name="ChoiceLab",
        phase="Research & Development",
        message="Decision-support features are intentionally not available yet.",
    )
