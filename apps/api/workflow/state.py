from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from models.events import SimulationStatus
from models.scenario import RegretScenario


class SimulationState(BaseModel):
    simulation_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    status: SimulationStatus = SimulationStatus.PENDING
    scenario: RegretScenario | None = None

    # Agent outputs
    plan: dict[str, Any] = Field(default_factory=dict)
    timeline_data: dict[str, Any] = Field(default_factory=dict)
    macro_data: dict[str, Any] = Field(default_factory=dict)
    industry_data: dict[str, Any] = Field(default_factory=dict)
    risk_data: dict[str, Any] = Field(default_factory=dict)
    narrative_data: dict[str, Any] = Field(default_factory=dict)

    # Universe state
    universe_state: dict[str, Any] = Field(default_factory=dict)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    # Error tracking
    error: str | None = None
    current_agent: str | None = None
