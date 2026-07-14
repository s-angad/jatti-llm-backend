from groq import AsyncGroq
from app.llm.provider import LLMProvider
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

class GroqProvider(LLMProvider):
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.groq_api_key)
        self.model = settings.model_name
        
    async def generate(self, prompt: str, max_tokens: int = settings.max_new_tokens, temperature: float = settings.temperature) -> str:
        if not settings.groq_api_key:
            logger.warning("GROQ_API_KEY is not set. Generation will fail.")
            
        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"GroqProvider generation failed: {e}")
            raise e
