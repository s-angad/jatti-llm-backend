#!/usr/bin/env python3
"""Interactive terminal tester for Jatti generation and validation."""

import sys

from app.context_store import ContextStore
from app.validator import JattiValidator
from app.rag import init_rag


def read_multiline_input(header: str) -> str:
    """Read multi-line input from the terminal until END is entered."""
    print(header)
    print("Enter lines of text. Type END on a new line to finish.")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def load_model_service():
    """Load the model service only when the user wants generation."""
    try:
        from app.model_service import ModelConfig, ModelService
    except Exception as exc:
        raise RuntimeError(
            f"Model dependencies are unavailable: {exc}. "
            "You can still use validation-only mode."
        ) from exc

    config = ModelConfig(
        max_new_tokens=256,
        temperature=0.2,
    )
    model_service = ModelService(config)
    model_service.load()
    return model_service


def run_generation_flow(prompt: str) -> None:
    """Generate code from a user prompt and validate it."""
    print("\nLoading RAG context...")
    context = ContextStore().load()
    print("✓ Context loaded")

    print("Loading validator...")
    validator = JattiValidator()
    print("✓ Validator ready")

    print("Initializing Semantic RAG...")
    init_rag(context)
    print("✓ RAG initialized")

    try:
        print("Loading Qwen model...")
        model_service = load_model_service()
        print("✓ Model loaded")

        print("\nGenerating code with model...\n")
        code = model_service.generate(
            prompt,
            context,
            max_new_tokens=256,
            temperature=0.2,
        )

    except Exception as exc:
        print(f"Model generation failed: {exc}")
        return

    print("=" * 70)
    print("GENERATED CODE")
    print("=" * 70)
    print(code)

    errors = validator.validate(code)
    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)
    if errors:
        print("✗ INVALID")
        for error in errors:
            print(f"  └─ {error}")
    else:
        print("✓ VALID")
        print("  └─ No errors found")


def run_validation_flow(code: str) -> None:
    """Validate pasted Jatti code from the terminal."""
    print("Loading validator...")
    validator = JattiValidator()
    errors = validator.validate(code)

    print("\n" + "=" * 70)
    print("CODE")
    print("=" * 70)
    print(code)

    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)
    if errors:
        print("✗ INVALID")
        for error in errors:
            print(f"  └─ {error}")
    else:
        print("✓ VALID")
        print("  └─ No errors found")


def main() -> int:
    print("=" * 70)
    print("JATTI TERMINAL TESTER (Qwen 1.5B + Semantic RAG)")
    print("=" * 70)
    print("Choose a test mode:")
    print("  1) Generate code from a natural-language prompt")
    print("  2) Validate pasted Jatti code")
    print("  3) Exit")

    choice = input("Select 1-3: ").strip()

    if choice == "1":
        prompt = input("Enter your prompt: ").strip()
        if not prompt:
            print("No prompt entered.")
            return 1
        try:
            run_generation_flow(prompt)
        except Exception as exc:
            print(f"ERROR: {exc}")
            return 1
        return 0

    if choice == "2":
        code = read_multiline_input("Paste your Jatti code:")
        if not code:
            print("No code entered.")
            return 1
        try:
            run_validation_flow(code)
        except Exception as exc:
            print(f"ERROR: {exc}")
            return 1
        return 0

    print("Exiting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())