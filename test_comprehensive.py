#!/usr/bin/env python3
"""Comprehensive test suite for Jatti code validator."""

import json
from pathlib import Path
from app.validator import JattiValidator
from app.context_store import ContextStore

def load_test_cases():
    """Load test cases from JSONL file."""
    test_file = Path("data/compiler_test_cases.jsonl")
    cases = []
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                cases.append(json.loads(line))
    return cases

def run_test_suite():
    """Run all test cases and report results."""
    print("=" * 70)
    print("JATTI CODE VALIDATOR - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    validator = JattiValidator()
    test_cases = load_test_cases()
    
    passed = 0
    failed = 0
    
    # Test 1: Compiler test cases from JSONL
    print("\n[TEST GROUP 1] Compiler Test Cases from JSONL")
    print("-" * 70)
    for idx, test_case in enumerate(test_cases, 1):
        code = test_case['input']
        expected = test_case['expected']
        notes = test_case['notes']
        
        errors = validator.validate(code)
        is_valid = len(errors) == 0
        result_str = "valid" if is_valid else "invalid"
        match = "✓ PASS" if result_str == expected else "✗ FAIL"
        
        print(f"\n  Test {idx}: {notes}")
        print(f"  Expected: {expected}, Got: {result_str} {match}")
        if errors:
            for error in errors:
                print(f"    └─ Error: {error}")
        
        if result_str == expected:
            passed += 1
        else:
            failed += 1
    
    # Test 2: Additional manual test cases
    print("\n" + "=" * 70)
    print("[TEST GROUP 2] Additional Manual Test Cases")
    print("-" * 70)
    
    additional_tests = [
        {
            "name": "Loop with har_ek",
            "code": """sun_we
    har_ek ginti ban [1, 2, 3]
        chilla_we ginti
ja_we""",
            "should_be": "valid"
        },
        {
            "name": "Function with multiple params",
            "code": """sun_we
    kaam multiply(a, b, c)
        wapas_kar a + b + c
    chilla_we multiply(2, 3, 4)
ja_we""",
            "should_be": "valid"
        },
        {
            "name": "Try-catch block",
            "code": """sun_we
    pakad try_this
        chal_oye x ban 10
    vichaar galti
        chilla_we "error"
ja_we""",
            "should_be": "valid"
        },
        {
            "name": "Missing sun_we keyword",
            "code": """    chilla_we "hello"
ja_we""",
            "should_be": "invalid"
        },
        {
            "name": "Tabs instead of spaces",
            "code": """sun_we
\tchilla_we "bad"
ja_we""",
            "should_be": "invalid"
        },
        {
            "name": "Nested if statement",
            "code": """sun_we
    je sach
        je sach
            chilla_we "nested"
ja_we""",
            "should_be": "valid"
        },
        {
            "name": "Invalid - chal_oye without ban",
            "code": """sun_we
    chal_oye x 10
ja_we""",
            "should_be": "invalid"
        },
        {
            "name": "Valid - Multiple statements",
            "code": """sun_we
    chal_oye x ban 10
    chal_oye y ban 20
    chal_oye z ban x + y
    chilla_we z
ja_we""",
            "should_be": "valid"
        }
    ]
    
    for idx, test in enumerate(additional_tests, 1):
        code = test['code']
        should_be = test['should_be']
        
        errors = validator.validate(code)
        is_valid = len(errors) == 0
        result_str = "valid" if is_valid else "invalid"
        match = "✓ PASS" if result_str == should_be else "✗ FAIL"
        
        print(f"\n  Test {idx}: {test['name']}")
        print(f"  Expected: {should_be}, Got: {result_str} {match}")
        if errors:
            for error in errors:
                print(f"    └─ Error: {error}")
        
        if result_str == should_be:
            passed += 1
        else:
            failed += 1
    
    # Test 3: RAG Context Loading
    print("\n" + "=" * 70)
    print("[TEST GROUP 3] RAG Context Loading")
    print("-" * 70)
    try:
        context_store = ContextStore()
        context = context_store.load()
        
        print("\n  ✓ Context loaded successfully")
        print(f"    └─ Grammar rules: {len(context.grammar_rules)} characters")
        print(f"    └─ Syntax docs: {len(context.syntax_docs)} characters")
        print(f"    └─ Examples: {len(context.examples)} characters")
        print(f"    └─ Test cases: {len(context.test_cases)} characters")
        passed += 1
    except Exception as e:
        print(f"\n  ✗ Context loading failed: {e}")
        failed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    total = passed + failed
    print(f"Total Tests: {total}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    if total > 0:
        percentage = (passed / total) * 100
        print(f"Success Rate: {percentage:.1f}%")
    print("=" * 70)
    
    return failed == 0

if __name__ == "__main__":
    success = run_test_suite()
    exit(0 if success else 1)
