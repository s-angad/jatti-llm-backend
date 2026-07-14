from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .context_store import ContextBundle
from .prompts import build_generation_prompt


@dataclass
class ModelConfig:
    model_name: str = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
    max_new_tokens: int = 512
    temperature: float = 0.2


class ModelService:
    def __init__(self, config: ModelConfig | None = None):
        self.config = config or ModelConfig()
        self.tokenizer = None
        self.model = None
        self.model_loaded = False
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load(self) -> None:
        if self.model_loaded:
            return

        kwargs = {"trust_remote_code": True}
        if torch.cuda.is_available():
            kwargs["device_map"] = "auto"
            kwargs["torch_dtype"] = torch.float16
            try:
                kwargs["load_in_4bit"] = True
            except Exception:
                pass
        else:
            kwargs["torch_dtype"] = torch.float32

        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.config.model_name, **kwargs)
        self.model_loaded = True

    def generate(self, prompt: str, context: ContextBundle, extra_context: str = "", max_new_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        if not self.model_loaded:
            self.load()

        full_prompt = build_generation_prompt(prompt, context, extra_context=extra_context)
        max_input_tokens = 768
        if hasattr(self.tokenizer, "model_max_length") and isinstance(self.tokenizer.model_max_length, int):
            if self.tokenizer.model_max_length > 0:
                max_input_tokens = min(max_input_tokens, self.tokenizer.model_max_length)

        inputs = self.tokenizer(
            full_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=max_input_tokens,
        )
        if self.device == "cuda" and hasattr(inputs, "to"):
            inputs = inputs.to("cuda")

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens or self.config.max_new_tokens,
            temperature=temperature if temperature is not None else self.config.temperature,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        if full_prompt in text:
            text = text.split(full_prompt, 1)[-1]
        return self._extract_code(text)

    def explain(self, code: str) -> str:
        return (
            "This code was generated locally by the model and should follow Jatti syntax. "
            "Use the validator to confirm structure and indentation.\n\n"
            f"Code summary: {code[:400]}"
        )

    @staticmethod
    def _extract_code(text: str) -> str:
        """Extract Jatti code from model output, removing prompt text."""
        cleaned = text.strip()
        
        # Remove system prompt and structure if it's still there
        if "[Output Rules]" in cleaned:
            after_rules = cleaned.split("[Output Rules]", 1)[-1]
            cleaned = after_rules.strip()
        
        # Try to find content after [User Request] section (prompt boundary)
        if "[User Request]" in cleaned:
            after_request = cleaned.split("[User Request]", 1)[-1]
            if "sun_we" in after_request:
                cleaned = after_request.strip()
        
        # Look for code blocks with triple backticks
        if "```" in cleaned:
            parts = cleaned.split("```")
            for part in parts[1:]:  # Skip first part before ``` marker
                if "sun_we" in part:
                    code = part.strip().strip("jatti").strip()
                    if code.startswith("sun_we") and code.count('\n') > 1:
                        return code
        
        # Find sun_we that marks start of actual code (not in markdown/text)
        # Look for lines that start with indentation or sun_we
        lines = cleaned.split('\n')
        code_started = False
        code_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Code starts with sun_we
            if stripped == "sun_we":
                code_started = True
                code_lines = [line]
            elif code_started:
                code_lines.append(line)
                # Code ends with ja_we
                if stripped == "ja_we":
                    return '\n'.join(code_lines).strip()
        
        # Fallback: look for sun_we...ja_we if we have them
        if "sun_we" in cleaned and "ja_we" in cleaned:
            # Find the LAST occurrence pattern (likely the actual code, not the examples)
            last_sun_we = cleaned.rfind("sun_we")
            last_ja_we = cleaned.rfind("ja_we")
            if last_sun_we >= 0 and last_ja_we > last_sun_we:
                # Make sure it looks like actual code (has more than just structure)
                potential = cleaned[last_sun_we:last_ja_we + len("ja_we")].strip()
                # Check if it has actual code (more than just the wrapper)
                if potential.count('\n') > 1:
                    return potential
        
        return cleaned
