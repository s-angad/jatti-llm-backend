from pathlib import Path

from app.context_store import ContextStore
from app.model_service import ModelService, ModelConfig
from app.validator import JattiValidator


def main() -> None:
    prompt = "create a jatti code for factorial number"
    context = ContextStore(Path(__file__).resolve().parent / "data").load()
    model = ModelService(ModelConfig())
    validator = JattiValidator()

    print("Loading model...")
    code = model.generate(prompt, context)
    print("\n=== Generated Jatti Code ===\n")
    print(code)

    print("\n=== Validation ===\n")
    errors = validator.validate(code)
    if errors:
        print("Invalid:")
        for err in errors:
            print("-", err)
    else:
        print("Valid")


if __name__ == "__main__":
    main()
