from app.memory.context_manager import context_manager

SYSTEM_PROMPT = """You are Jatti-AI, an expert AI coding assistant for the Jatti programming language.
Jatti is a Punjabi-based programming language.

CRITICAL RULES:
1. Every Jatti program MUST begin with `sun_we` on the first line.
2. Every Jatti program MUST end with `ja_we` on the last line.
3. You MUST use EXACTLY 4 spaces for indentation inside all blocks. Since `sun_we` and `ja_we` act as the main function, EVERY single line of code between them MUST be indented by 4 spaces. Do not use tabs.
4. Variables are assigned using `chal_oye <name> ban <value>`.
5. Keep the code as simple and direct as possible. Do not overcomplicate simple requests with unnecessary variables.
6. Output ONLY the raw code. Do not include extra explanations or pleasantries."""

def build_prompt(user_query: str, retrieved_docs: list[str]) -> tuple[str, str]:
    system = SYSTEM_PROMPT + "\n\n"
    
    if retrieved_docs:
        system += "Language Documentation and Examples:\n"
        for doc in retrieved_docs:
            system += f"{doc}\n---\n"
            
    # Always read the grammar rules directly to enforce strictness
    try:
        with open("data/grammar_rules.md", "r") as f:
            grammar = f.read()
            system += f"\n[Strict Grammar Rules - DO NOT VIOLATE]\n{grammar}\n"
    except Exception:
        pass
        
    user = f"User Request: {user_query}\nJatti Code:\n"
    return system, user
