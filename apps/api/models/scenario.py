from __future__ import annotations

from pydantic import BaseModel, Field


class RegretScenario(BaseModel):
    choice_point: str = Field(
        ...,
        description="用户后悔的那个选择点，例如：'2018年放弃去深圳腾讯'",
        min_length=2,
        max_length=500,
    )
    time_node: str = Field(
        ...,
        description="时间节点，格式：YYYY-MM，例如：'2018-06'",
        pattern=r"^\d{4}-(0[1-9]|1[0-2])$",
    )
    alternative: str = Field(
        ...,
        description="如果做了另一个选择会怎样，例如：'接受腾讯 offer 去深圳'",
        min_length=2,
        max_length=500,
    )
    current_state: str = Field(
        ...,
        description="当前人生状态描述",
        min_length=2,
        max_length=1000,
    )
    user_age_at_time: int | None = Field(
        None,
        description="当时年龄",
        ge=10,
        le=80,
    )
    user_education: str | None = Field(
        None,
        description="当时学历",
        max_length=200,
    )
    user_industry: str | None = Field(
        None,
        description="当时所在行业",
        max_length=200,
    )
    user_city: str | None = Field(
        None,
        description="当时所在城市",
        max_length=100,
    )


class SimulationRequest(BaseModel):
    scenario: RegretScenario
    depth: int = Field(
        default=5,
        description="推演深度（时间线节点数量）",
        ge=3,
        le=15,
    )
    include_narrative: bool = Field(
        default=True,
        description="是否生成叙事文本",
    )
