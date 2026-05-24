from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DimensionScore(BaseModel):
    dimension: str = Field(..., description="维度名称")
    original_score: float = Field(..., ge=0.0, le=100.0)
    alternative_score: float = Field(..., ge=0.0, le=100.0)
    description: str = ""


class UniverseState(BaseModel):
    universe_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    simulation_id: str = ""

    # 原始宇宙状态
    original_title: str = Field("原始时间线", description="原始宇宙标题")
    original_summary: str = ""
    original_financial_trajectory: list[float] = Field(
        default_factory=list,
        description="原始时间线的财务轨迹（月薪序列）",
    )

    # 平行宇宙状态
    alternative_title: str = Field("平行时间线", description="平行宇宙标题")
    alternative_summary: str = ""
    alternative_financial_trajectory: list[float] = Field(
        default_factory=list,
        description="平行时间线的财务轨迹（月薪序列）",
    )

    # 维度对比
    dimensions: list[DimensionScore] = Field(
        default_factory=list,
        description="各维度对比评分",
    )

    # 核心洞察
    key_insight: str = ""
    regret_score: float = Field(
        default=50.0,
        ge=0.0,
        le=100.0,
        description="后悔指数，0=完全不后悔，100=极度后悔",
    )
    growth_potential: float = Field(
        default=50.0,
        ge=0.0,
        le=100.0,
        description="成长潜力指数",
    )

    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UniverseComparison(BaseModel):
    simulation_id: str
    original: UniverseState
    alternative: UniverseState
    comparison_summary: str = ""
    recommendation: str = ""
