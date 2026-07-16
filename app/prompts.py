from __future__ import annotations

from .context_store import ContextBundle
from .rag import get_rag

SYSTEM_PROMPT = """You are an expert Jatti language code generator.
CRITICAL INSTRUCTIONS:
1. Return ONLY valid Jatti code based on the user's request.
2. Jatti has strict syntax. YOU MUST NEVER hallucinate Python, JS, or C++ keywords.
3. ALWAYS output a complete program starting with `sun_we` and ending with `ja_we` unless specifically asked for a snippet.
4. Use 4-space indentation.
5. Do not wrap your code in markdown blocks unless required, but if you do, use ```jatti
"""

def build_generation_prompt(user_prompt: str, context: ContextBundle, extra_context: str = "") -> str:
    rag = get_rag()
    
    if rag:
        retrieved_context_list = rag.retrieve(user_prompt, top_k=5)
        examples_context = "\n\n".join(retrieved_context_list)
    else:
        # Fallback if RAG is not initialized
        examples_context = context.examples[:1000]

    # Always inject the full grammar rules for absolute strictness, plus the examples
    retrieved_context = (
        "[Strict Grammar Rules - DO NOT VIOLATE]\n" + context.grammar_rules + 
        "\n\n[Relevant Examples]\n" + examples_context
    )
        
    extra_block = f"\n[User Context]\n{extra_context}\n" if extra_context.strip() else ""

    return f"""<|im_start|>system
{SYSTEM_PROMPT}

Here is the relevant Jatti documentation and examples to help you:
{retrieved_context}
<|im_end|>
<|im_start|>user
{extra_block}
Request: {user_prompt.strip()}
<|im_end|>
<|im_start|>assistant
"""

def build_explain_prompt(code: str) -> str:
    return f"""<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
Explain the following Jatti code in plain English.

[Jatti Code]
{code.strip()}
<|im_end|>
<|im_start|>assistant
"""
