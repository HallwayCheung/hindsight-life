from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from models.events import AgentEvent, AgentName, AgentStatus, EventType
from services.dashscope import dashscope_service
from core.logging import get_logger


class BaseAgent(ABC):
    def __init__(self, agent_name: AgentName):
        self.name = agent_name
        self.logger = get_logger(agent_name.value)
        self.llm = dashscope_service

    async def emit_event(
        self,
        event_type: EventType,
        status: AgentStatus,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> AgentEvent:
        event = AgentEvent(
            event_type=event_type,
            agent=self.name,
            status=status,
            message=message,
            data=data,
        )
        self.logger.info(f"[{status.value}] {message}")
        return event

    @abstractmethod
    async def execute(
        self,
        context: dict[str, Any],
    ) -> AsyncGenerator[AgentEvent, None]:
        """Execute the agent and yield events."""
        ...

    def _build_system_prompt(self) -> str:
        return ""

    def _build_messages(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> list[dict[str, str]]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        return messages
