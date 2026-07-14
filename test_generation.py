#!/usr/bin/env python3
import sys
import asyncio
from app.services.generation_service import generation_service
from app.validator import JattiValidator

async def run_generation_flow(prompt: str) -> None:
    print(f"\nGenerating code with Hugging Face Provider...")
    result = await generation_service.generate_code(prompt, max_tokens=256)
    
    print("=" * 70)
    print("GENERATED CODE")
    print("=" * 70)
    print(result.get("code", "ERROR: " + result.get("error", "")))
    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)
    if not result.get("valid"):
        print("✗ INVALID")
        for error in result.get("validation_errors", []):
            print(f"  └─ {error}")
    else:
        print("✓ VALID")
        print("  └─ No errors found")

def main() -> int:
    print("=" * 70)
    print("JATTI TERMINAL TESTER (Cloud RAG)")
    print("=" * 70)
    prompt = input("Enter your prompt: ").strip()
    if not prompt:
        return 1
        
    asyncio.run(run_generation_flow(prompt))
    return 0

if __name__ == "__main__":
    sys.exit(main())