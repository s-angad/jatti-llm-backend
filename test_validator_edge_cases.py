#!/usr/bin/env python3
"""Test suite without LLM - just validator tests."""

import json
from pathlib import Path

# Import validator directly
import sys
sys.path.insert(0, 'app')

from validator import JattiValidator
from context_store import ContextStore

def run_edge_case_tests():
    """Run edge case tests."""
    print("=" * 70)
    print("JATTI CODE VALIDATOR - EDGE CASE AND STRESS TESTS")
    print("=" * 70)
    
    validator = JattiValidator()
    
    test_cases = {
        "Empty program": ("sun_we\nja_we", "valid"),
        "Single statement": ("sun_we\n    chilla_we 1\nja_we", "valid"),
        "Deep nesting": ("""sun_we
    je sach
        je sach
            je sach
                chilla_we "deep"
ja_we""", "valid"),
        "Long variable names": ("""sun_we
    chal_oye my_very_long_variable_name_here ban 123
    chilla_we my_very_long_variable_name_here
ja_we""", "valid"),
        "Multiple functions": ("""sun_we
    kaam func1()
        wapas_kar 1
    kaam func2()
        wapas_kar 2
    chilla_we func1()
ja_we""", "valid"),
        "Comments": ("""sun_we
    # This is a comment
    chilla_we "hello"
ja_we""", "valid"),
        "Missing ja_we at EOF": ("""sun_we
    chilla_we "test\"""", "invalid"),
        "No sun_we": ("""    chilla_we "hello"
ja_we""", "invalid"),
        "Mixed spacing": ("""sun_we
    chal_oye x ban 1
        chilla_we x
ja_we""", "invalid"),
        "Function without params": ("""sun_we
    kaam dosomething
        chilla_we "hi"
ja_we""", "valid"),
    }
    
    passed = 0
    failed = 0
    
    for name, (code, expected) in test_cases.items():
        errors = validator.validate(code)
        is_valid = len(errors) == 0
        result = "valid" if is_valid else "invalid"
        match = "✓" if result == expected else "✗"
        
        status = f"{match} {result.upper()} (expected {expected})"
        passed += 1 if result == expected else 0
        failed += 0 if result == expected else 1
        
        print(f"\n{name}: {status}")
        if errors:
            for error in errors:
                print(f"  └─ {error}")
    
    return passed, failed

def test_context_loading():
    """Test context loading."""
    print("\n" + "=" * 70)
    print("CONTEXT LOADING TEST")
    print("=" * 70)
    
    context_store = ContextStore()
    context = context_store.load()
    
    print(f"\n✓ Grammar Rules: {len(context.grammar_rules)} bytes")
    print(f"✓ Syntax Docs: {len(context.syntax_docs)} bytes")
    print(f"✓ Examples: {len(context.examples)} bytes")
    print(f"✓ Test Cases: {len(context.test_cases)} bytes")
    print(f"\nTotal RAG Context: {len(context.as_prompt_block())} bytes")
    
    return True

def main():
    try:
        # Run edge case tests
        passed, failed = run_edge_case_tests()
        
        # Test context loading
        context_ok = test_context_loading()
        
        # Summary
        total = passed + failed
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Edge Cases: {passed}/{total} passed ({100*passed//total}%)")
        print(f"Context Loading: {'✓ OK' if context_ok else '✗ FAILED'}")
        print("=" * 70)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
