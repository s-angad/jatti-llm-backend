import httpx
from app.llm.provider import LLMProvider
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

class HFProvider(LLMProvider):
    def __init__(self):
        self.model = settings.default_model
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {settings.hf_token}"}
        
    async def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.1) -> str:
        if not settings.hf_token:
            logger.warning("HF_TOKEN is not set. Generation might fail due to rate limits.")
            
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.api_url, headers=self.headers, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
                    return data[0]["generated_text"]
                elif "error" in data:
                    raise Exception(f"HF API Error: {data['error']}")
                else:
                    return str(data)
            except Exception as e:
                logger.error(f"HFProvider generation failed: {e}")
                raise e
