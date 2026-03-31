from typing import Literal

from pydantic import BaseModel, Field


class LogRequest(BaseModel):
    log: str = Field(
        ...,
        description="Raw infrastructure or application log content to analyze.",
        min_length=1,
    )


class LogAnalysis(BaseModel):
    issue: str = Field(..., description="Short issue name.")
    cause: str = Field(..., description="Root cause explanation.")
    fix: str = Field(..., description="Actionable remediation step.")
    severity: Literal["Low", "Medium", "High", "Critical"] = Field(
        ...,
        description="Estimated operational severity.",
    )
