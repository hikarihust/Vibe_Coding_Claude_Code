from typing import AsyncIterator

from ollama import AsyncClient

MODEL = "gemma4:31b-cloud"


async def stream_chat(messages: list[dict]) -> AsyncIterator[str]:
    async for part in await AsyncClient().chat(model=MODEL, messages=messages, stream=True):
        if part.message.content:
            yield part.message.content
