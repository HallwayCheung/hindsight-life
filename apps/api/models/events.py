from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentName(str, Enum):
    PLANNER = "planner"
    TIMELINE = "timeline"
    MACRO_ECONOMY = "macro_economy"
    INDUSTRY = "industry"
    RISK = "risk"
    NARRATIVE = "narrative"


class AgentStatus(str, Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    COMPLETE = "complete"
    ERROR = "error"


class EventType(str, Enum):
    AGENT_START = "agent_start"
    AGENT_PROGRESS = "agent_progress"
    AGENT_COMPLETE = "agent_complete"
    TIMELINE_NODE = "timeline_node"
    NARRATIVE_CHUNK = "narrative_chunk"
    SIMULATION_COMPLETE = "simulation_complete"
    SIMULATION_ERROR = "simulation_error"


class AgentEvent(BaseModel):
    event_type: EventType
    agent: AgentName
    status: AgentStatus
    message: str
    data: dict[str, Any] | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])

    def to_sse(self) -> dict[str, str]:
        return {
            "event": self.event_type.value,
            "data": self.model_dump_json(),
        }


class NarrativeChunk(BaseModel):
    chunk_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    text: str
    year: int | None = None
    narrative_type: str = "story"  # story, analysis, reflection
    is_final: bool = False


class SimulationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    ERROR = "error"


class SimulationResult(BaseModel):
    simulation_id: str
    status: SimulationStatus
    timeline: list[TimelineNode] = []
    universe_state: UniverseState | None = None
    narrative: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None


from .timeline import TimelineNode  # noqa: E402
from .universe import UniverseState  # noqa: E402

SimulationResult.model_rebuild()
