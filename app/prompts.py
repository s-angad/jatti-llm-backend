from __future__ import annotations

from .context_store import ContextBundle
from .rag import get_rag

SYSTEM_PROMPT = """You are an expert Jatti language code generator.
Return only valid Jatti code based on the user's request.
Always output a complete Jatti program using sun_we and ja_we.
Use 4-space indentation.
Do not wrap your code in markdown blocks unless required, but if you do, use ```jatti
"""

def build_generation_prompt(user_prompt: str, context: ContextBundle, extra_context: str = "") -> str:
    rag = get_rag()
    
    if rag:
        retrieved_context = rag.retrieve(user_prompt, top_k=5)
    else:
        # Fallback if RAG is not initialized
        retrieved_context = (
            "[Grammar Rules]\n" + context.grammar_rules[:500] + 
            "\n\n[Examples]\n" + context.examples[:1000]
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
