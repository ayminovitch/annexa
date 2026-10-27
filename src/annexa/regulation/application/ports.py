from typing import Protocol


class EmbeddingProvider(Protocol):
    """
    Port: Abstraction for generating vector embeddings from text.
    The Application layer depends on this, not on google-genai directly.
    """
    async def generate_embedding(self, text: str) -> list[float]:
        ...

class LLMProvider(Protocol):
    """
    Port: Abstraction for text generation
    """
    async def generate_text(self, prompt: str) -> str:
        ...