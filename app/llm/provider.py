from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list, max_tokens: int = 500, temperature: float = 0.2) -> str:
        pass
