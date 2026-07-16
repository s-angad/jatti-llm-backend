from app.rag.retriever import retriever
from app.prompts.builder import build_prompt
from app.llm.groq_provider import GroqProvider
from app.core.config import settings
from app.validator import JattiValidator # using old validator for now
from app.core.logger import get_logger

logger = get_logger(__name__)

class GenerationService:
    def __init__(self):
        self.provider = GroqProvider()
        self.validator = JattiValidator()
        
    async def generate_code(self, prompt: str, context: str = "", history: list = None, max_tokens: int = 500, temperature: float = 0.2) -> dict:
        if history is None:
            history = []
        try:
            # 1. Retrieve
            retrieved_docs = retriever.retrieve(prompt)
            
            # 2. Build Prompt
            system_msg, user_msg = build_prompt(prompt, retrieved_docs)
            
            if context:
                user_msg += f"\nUser Context:\n{context}\n"
                
            messages = [{"role": "system", "content": system_msg}]
            # Inject history
            for turn in history:
                if "user" in turn and "assistant" in turn:
                    messages.append({"role": "user", "content": turn["user"]})
                    messages.append({"role": "assistant", "content": turn["assistant"]})
                elif "role" in turn and "content" in turn:
                    messages.append({"role": turn["role"], "content": turn["content"]})
                    
            messages.append({"role": "user", "content": user_msg})
                
            # 3. Generate
            logger.info(f"Generating code with {self.provider.__class__.__name__}")
            generated_code = await self.provider.generate(messages, max_tokens, temperature)
            
            # 4. Clean, Format, and Validate
            clean_code = generated_code.replace("```jatti", "").replace("```", "").strip()
            
            # Auto-formatter for Jatti indentation rules
            lines = clean_code.splitlines()
            formatted_lines = []
            inside_main = False
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                    
                if stripped.startswith("sun_we"):
                    formatted_lines.append(stripped)
                    inside_main = True
                elif stripped.startswith("ja_we"):
                    formatted_lines.append(stripped)
                    inside_main = False
                elif inside_main:
                    # Enforce that it's indented by AT LEAST 4 spaces
                    # We look at the original indent relative to the stripped line
                    original_indent = len(line) - len(line.lstrip())
                    # If the LLM forgot to indent the main block, we shift it by 4
                    if original_indent == 0:
                        formatted_lines.append("    " + stripped)
                    else:
                        # Ensure it's a multiple of 4
                        adjusted_indent = ((original_indent + 3) // 4) * 4
                        # Ensure minimum 4 spaces inside sun_we
                        adjusted_indent = max(4, adjusted_indent)
                        formatted_lines.append(" " * adjusted_indent + stripped)
                else:
                    # Outside main (like imports or function defs if any)
                    original_indent = len(line) - len(line.lstrip())
                    adjusted_indent = ((original_indent + 3) // 4) * 4
                    formatted_lines.append(" " * adjusted_indent + stripped)
                    
            clean_code = "\n".join(formatted_lines)
            
            validation_errors = self.validator.validate(clean_code)
            
            validation_errors = self.validator.validate(clean_code)
            
            return {
                "success": True,
                "code": clean_code,
                "valid": len(validation_errors) == 0,
                "validation_errors": validation_errors
            }
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return {
                "success": False,
                "code": "",
                "error": str(e)
            }

generation_service = GenerationService()
