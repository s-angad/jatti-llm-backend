from __future__ import annotations

import argparse
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.schemas import (
    ExplainRequest,
    ExplainResponse,
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
    ValidateRequest,
    ValidateResponse,
)
from app.services.generation_service import generation_service
from app.core.config import settings
from app.core.logger import get_logger
from app.validator import JattiValidator

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Jatti Backend with provider: " + settings.llm_provider)
    yield
    logger.info("Shutting down Jatti Backend")

app = FastAPI(title="Jatti Cloud RAG Backend", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

validator = JattiValidator()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": settings.model_name,
        "groq_key": bool(os.getenv("GROQ_API_KEY")),
        "settings_key": bool(settings.groq_api_key),
    }

@app.post("/api/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    result = await generation_service.generate_code(
        prompt=request.prompt,
        context=request.context,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    if result["success"]:
        return GenerateResponse(success=True, code=result["code"])
    else:
        return GenerateResponse(success=False, error=result["error"])

@app.post("/api/validate", response_model=ValidateResponse)
def validate(request: ValidateRequest) -> ValidateResponse:
    errors = validator.validate(request.code)
    return ValidateResponse(valid=not errors, errors=errors)

@app.post("/api/explain", response_model=ExplainResponse)
async def explain(request: ExplainRequest) -> ExplainResponse:
    result = await generation_service.generate_code(
        prompt="Explain this Jatti code concisely.",
        context=request.code,
        max_tokens=300
    )
    return ExplainResponse(explanation=result["code"] if result["success"] else result["error"])

def main() -> None:
    parser = argparse.ArgumentParser(description="Run Jatti RAG backend")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    port = int(os.environ.get("PORT", args.port))
    host = "0.0.0.0" if os.environ.get("PORT") else args.host

    uvicorn.run("app.main:app", host=host, port=port, reload=args.reload)

def cli() -> None:
    main()
