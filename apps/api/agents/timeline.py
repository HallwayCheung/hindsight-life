from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from agents.base import BaseAgent
from models.events import AgentEvent, AgentName, AgentStatus, EventType
from models.scenario import RegretScenario


class TimelineAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentName.TIMELINE)

    def _build_system_prompt(self) -> str:
        return """你是一个时间线推演专家。你的任务是基于用户的后悔场景，生成两条平行时间线。

你需要生成：
1. 原始时间线：用户实际经历的人生轨迹
2. 平行时间线：如果做了另一个选择的人生轨迹

每条时间线包含多个节点，每个节点是人生中的关键事件。

输出格式（JSON）：
{
    "original_branch": {
        "label": "留在成都",
        "nodes": [
            {
                "year": 2018,
                "month": 6,
                "title": "拒绝腾讯offer",
                "description": "选择留在成都继续当前工作",
                "event_type": "career",
                "probability": 1.0,
                "impact_score": -0.3,
                "financial_impact": 0,
                "city": "成都"
            }
        ],
        "summary": "时间线总结"
    },
    "alternative_branch": {
        "label": "去深圳腾讯",
        "nodes": [...],
        "summary": "时间线总结"
    },
    "divergence_point": 2018,
    "key_differences": ["差异1", "差异2"]
}"""

    async def execute(
        self,
        context: dict[str, Any],
    ) -> AsyncGenerator[AgentEvent, None]:
        scenario: RegretScenario = context["scenario"]
        plan: dict[str, Any] = context.get("plan", {})

        yield await self.emit_event(
            EventType.AGENT_START,
            AgentStatus.THINKING,
            "正在构建平行时间线...",
        )

        user_prompt = f"""
用户场景：
- 后悔选择：{scenario.choice_point}
- 时间节点：{scenario.time_node}
- 替代选择：{scenario.alternative}
- 当前状态：{scenario.current_state}

推演计划：
- 时间跨度：{plan.get('time_span', {})}
- 关键维度：{plan.get('dimensions', [])}
- 关键因素：{plan.get('key_factors', [])}

请生成两条平行时间线，每条包含 5-8 个关键节点。
"""

        yield await self.emit_event(
            EventType.AGENT_PROGRESS,
            AgentStatus.GENERATING,
            "正在推演原始时间线...",
        )

        messages = self._build_messages(self._build_system_prompt(), user_prompt)
        timeline_data = await self.llm.chat_json(messages, temperature=0.5)

        # Emit individual timeline nodes
        for branch_key in ["original_branch", "alternative_branch"]:
            branch = timeline_data.get(branch_key, {})
            for node in branch.get("nodes", []):
                yield await self.emit_event(
                    EventType.TIMELINE_NODE,
                    AgentStatus.GENERATING,
                    f"{node.get('year')}年：{node.get('title')}",
                    data={"branch": branch_key, "node": node},
                )

        yield await self.emit_event(
            EventType.AGENT_COMPLETE,
            AgentStatus.COMPLETE,
            f"时间线生成完成，分歧点：{timeline_data.get('divergence_point')}年",
            data=timeline_data,
        )
