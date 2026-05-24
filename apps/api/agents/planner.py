from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from agents.base import BaseAgent
from models.events import AgentEvent, AgentName, AgentStatus, EventType
from models.scenario import RegretScenario


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentName.PLANNER)

    def _build_system_prompt(self) -> str:
        return """你是一个人生推演规划师。你的任务是分析用户的后悔场景，制定推演计划。

你需要：
1. 理解用户的选择点和替代选择
2. 识别需要推演的关键维度（职业、财务、生活、关系等）
3. 确定推演的时间跨度和关键节点
4. 为后续 Agent 提供结构化的推演框架

输出格式（JSON）：
{
    "analysis": "对用户场景的分析",
    "dimensions": ["career", "financial", "lifestyle", "relationship"],
    "time_span": {"start": 2018, "end": 2024},
    "key_factors": ["行业趋势", "城市选择", "职业发展"],
    "risk_factors": ["黑天鹅事件", "行业周期"],
    "recommended_depth": 6,
    "planning_notes": "推演计划说明"
}"""

    async def execute(
        self,
        context: dict[str, Any],
    ) -> AsyncGenerator[AgentEvent, None]:
        scenario: RegretScenario = context["scenario"]

        yield await self.emit_event(
            EventType.AGENT_START,
            AgentStatus.THINKING,
            f"正在分析你的后悔场景：{scenario.choice_point}",
        )

        user_prompt = f"""
用户后悔的选择点：{scenario.choice_point}
时间节点：{scenario.time_node}
替代选择：{scenario.alternative}
当前状态：{scenario.current_state}
当时年龄：{scenario.user_age_at_time or '未知'}
学历：{scenario.user_education or '未知'}
行业：{scenario.user_industry or '未知'}
城市：{scenario.user_city or '未知'}

请制定推演计划。
"""

        yield await self.emit_event(
            EventType.AGENT_PROGRESS,
            AgentStatus.ANALYZING,
            "正在构建推演框架和维度...",
        )

        messages = self._build_messages(self._build_system_prompt(), user_prompt)
        plan = await self.llm.chat_json(messages, temperature=0.3)

        yield await self.emit_event(
            EventType.AGENT_PROGRESS,
            AgentStatus.ANALYZING,
            f"已识别 {len(plan.get('dimensions', []))} 个推演维度",
            data=plan,
        )

        yield await self.emit_event(
            EventType.AGENT_COMPLETE,
            AgentStatus.COMPLETE,
            "推演计划制定完成",
            data=plan,
        )
