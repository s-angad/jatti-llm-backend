from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    context: str = ""
    max_tokens: int = 1000
    temperature: float = 0.2


class GenerateResponse(BaseModel):
    success: bool
    code: str = ""
    error: Optional[str] = None


class ValidateRequest(BaseModel):
    code: str = Field(..., min_length=1)


class ValidateResponse(BaseModel):
    valid: bool
    errors: List[str] = Field(default_factory=list)


class ExplainRequest(BaseModel):
    code: str = Field(..., min_length=1)


class ExplainResponse(BaseModel):
    explanation: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
