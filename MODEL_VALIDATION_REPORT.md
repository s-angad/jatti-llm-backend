# Jatti Model Validation Report

## Scope
Validate the current Jatti code-generation pipeline, including model output quality, fallback behavior, and runtime support for common language features.

## Tested Areas
- Natural-language to Jatti code generation
- Validation of generated code
- Loop generation
- Function generation
- String handling via `vand_karo`
- Runtime execution of generated Jatti code

## Summary
- The model loads successfully.
- The model often produces non-Jatti or incomplete output.
- The fallback generator reliably produces valid Jatti code.
- The validator catches invalid model output before it is accepted.
- `vand_karo` is implemented in the runtime and works with non-empty delimiters.

## Observed Results

| Test | Result | Notes |
|---|---:|---|
| Model load | Pass | `gpt2` loads successfully in the backend |
| Loop prompt | Pass | Invalid model output replaced by fallback; final code validated |
| While-loop sum prompt | Pass | Fallback produced valid Jatti and validation passed |
| Sentence-to-words prompt | Pass | Fallback produced valid function-based Jatti and validation passed |

## Model Quality Assessment
### Strengths
- Produces output in the expected workflow when the prompt is simple.
- Works better when the prompt is heavily guided by examples and task-specific context.

### Weaknesses
- Frequently fails to produce valid Jatti syntax directly.
- Can confuse task intent, especially on function/string/loop combinations.
- Requires fallback logic for reliable generation.

## Reliability Assessment
- **Direct model reliability:** Low to moderate
- **End-to-end reliability with fallback:** High
- **Validator effectiveness:** High

## Conclusion
The current model is not yet strong enough to be considered fully reliable for direct Jatti generation on its own. However, the overall system is usable and stable because:
1. prompt routing is task-aware,
2. the validator rejects invalid output,
3. the fallback generator guarantees valid Jatti code.

## Recommendation
- Keep the fallback generator enabled.
- Continue improving prompt routing and examples.
- If higher direct model quality is needed, replace `gpt2` with a stronger code-focused model.
