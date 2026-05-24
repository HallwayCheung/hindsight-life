from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TimelineNode(BaseModel):
    node_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    year: int = Field(..., ge=1990, le=2050)
    month: int | None = Field(None, ge=1, le=12)
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=2000)
    event_type: str = Field(
        default="life_event",
        description="事件类型：career, life_event, financial, relationship, health, black_swan",
    )
    probability: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="该节点发生的概率",
    )
    impact_score: float = Field(
        default=0.5,
        ge=-1.0,
        le=1.0,
        description="影响得分，正为积极，负为消极",
    )
    financial_impact: float | None = Field(
        None,
        description="财务影响（元/月）",
    )
    city: str | None = None
    industry: str | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TimelineBranch(BaseModel):
    branch_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    label: str = Field(..., description="分支名称，如'选择了腾讯'或'留在成都'")
    nodes: list[TimelineNode] = Field(default_factory=list)
    summary: str = ""
    overall_score: float = Field(default=0.0, ge=-1.0, le=1.0)


class TimelineData(BaseModel):
    timeline_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    scenario_description: str = ""
    original_branch: TimelineBranch = Field(
        ...,
        description="原始时间线（用户实际经历的）",
    )
    alternative_branch: TimelineBranch = Field(
        ...,
        description="平行时间线（如果做了另一个选择）",
    )
    divergence_point: int = Field(
        ...,
        description="两条时间线的分歧年份",
    )
    key_differences: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
