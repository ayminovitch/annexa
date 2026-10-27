from collections.abc import AsyncGenerator
from google import genai

from annexa.config.settings import settings
from annexa.regulation.application.ports import LLMProvider

class GoogleGenAIProvider(LLMProvider):
    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.gemini_api_key)

    async def generate_text(self, prompt: str) -> str:
        response = await self._client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents = prompt,
        )

        return response.text or ""

    async def generate_text_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        response = await self._client.aio.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents = prompt,
        )

        async for chunk in response:
            if chunk.text:
                yield chunk.text

