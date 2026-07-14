from __future__ import annotations

import argparse
from pathlib import Path

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .context_store import ContextStore
from .model_service import ModelService, ModelConfig
from .schemas import (
    ExplainRequest,
    ExplainResponse,
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
    ValidateRequest,
    ValidateResponse,
)
from .validator import JattiValidator
from .rag import init_rag
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    context = context_store.load()
    init_rag(context)
    yield

app = FastAPI(title="Jatti Local LLM Backend", version="0.1.0", lifespan=lifespan)

# Add CORS middleware to allow the VS Code extension to connect from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
context_store = ContextStore()
validator = JattiValidator()
model_service = ModelService(ModelConfig())


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", model_loaded=model_service.model_loaded, model_name=model_service.config.model_name)


@app.post("/api/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    try:
        context = context_store.load()
        code = model_service.generate(
            request.prompt,
            context,
            extra_context=request.context,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        return GenerateResponse(success=True, code=code)
    except Exception as exc:
        return GenerateResponse(success=False, error=str(exc))


@app.post("/api/validate", response_model=ValidateResponse)
def validate(request: ValidateRequest) -> ValidateResponse:
    errors = validator.validate(request.code)
    return ValidateResponse(valid=not errors, errors=errors)


@app.post("/api/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest) -> ExplainResponse:
    return ExplainResponse(explanation=model_service.explain(request.code))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Jatti local LLM backend")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    # For deployment, bind to 0.0.0.0 and use the PORT environment variable if available
    port = int(os.environ.get("PORT", args.port))
    host = "0.0.0.0" if os.environ.get("PORT") else args.host

    uvicorn.run("app.main:app", host=host, port=port, reload=args.reload)


def cli() -> None:
    main()
