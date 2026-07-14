#!/usr/bin/env python3
import sys
print("Python:", sys.executable)
print("Version:", sys.version)

try:
    import transformers
    print("✓ transformers:", transformers.__version__)
except Exception as e:
    print("✗ transformers failed:", e)

try:
    import torch
    print("✓ torch:", torch.__version__)
except Exception as e:
    print("✗ torch failed:", e)

try:
    from transformers import AutoTokenizer
    print("✓ AutoTokenizer imported")
except Exception as e:
    print("✗ AutoTokenizer failed:", e)

try:
    from transformers import AutoModelForCausalLM
    print("✓ AutoModelForCausalLM imported")
except Exception as e:
    print("✗ AutoModelForCausalLM failed:", e)
    import traceback
    traceback.print_exc()

try:
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    print("✓ Tokenizer loaded")
except Exception as e:
    print("✗ Tokenizer load failed:", e)
