from __future__ import annotations

import json
from collections.abc import AsyncGenerator
from typing import Any

import dashscope
from dashscope import Generation

from config import get_settings
from core.logging import get_logger
from core.exceptions import DashScopeAPIError

logger = get_logger("dashscope")


class DashScopeService:
    def __init__(self):
        settings = get_settings()
        dashscope.api_key = settings.dashscope_api_key
        self.model = settings.dashscope_model

    async def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        try:
            response = Generation.call(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                result_format="message",
            )

            if response.status_code != 200:
                raise DashScopeAPIError(
                    message=response.message,
                    status_code=response.status_code,
                )

            return response.output.choices[0].message.content

        except DashScopeAPIError:
            raise
        except Exception as e:
            logger.error(f"DashScope API call failed: {e}")
            raise DashScopeAPIError(message=str(e))

    async def chat_stream(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> AsyncGenerator[str, None]:
        try:
            responses = Generation.call(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                result_format="message",
                stream=True,
                incremental_output=True,
            )

            for response in responses:
                if response.status_code != 200:
                    raise DashScopeAPIError(
                        message=response.message,
                        status_code=response.status_code,
                    )
                content = response.output.choices[0].message.content
                if content:
                    yield content

        except DashScopeAPIError:
            raise
        except Exception as e:
            logger.error(f"DashScope streaming call failed: {e}")
            raise DashScopeAPIError(message=str(e))

    async def chat_json(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4000,
    ) -> dict[str, Any]:
        raw = await self.chat(messages, temperature=temperature, max_tokens=max_tokens)
        try:
            # Extract JSON from possible markdown code blocks
            text = raw.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                text = "\n".join(lines[1:-1])
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON response: {raw[:200]}")
            raise DashScopeAPIError(message="Invalid JSON response from LLM")


dashscope_service = DashScopeService()
