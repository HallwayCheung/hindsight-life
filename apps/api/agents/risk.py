from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from agents.base import BaseAgent
from models.events import AgentEvent, AgentName, AgentStatus, EventType


class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentName.RISK)

    def _build_system_prompt(self) -> str:
        return """你是一个风险评估专家。你的任务是评估两条时间线中的风险和机遇。

你需要评估：
1. 职业风险（裁员、行业衰退）
2. 财务风险（投资失败、负债）
3. 健康风险（工作压力、生活平衡）
4. 关系风险（家庭、社交）
5. 黑天鹅事件影响
6. 每个选择的隐藏机遇

输出格式（JSON）：
{
    "original_risks": [
        {
            "risk_type": "career",
            "description": "传统行业数字化转型失败",
            "probability": 0.3,
            "impact": -0.5,
            "year": 2022
        }
    ],
    "alternative_risks": [...],
    "hidden_opportunities": [
        {
            "branch": "alternative",
            "opportunity": "AI浪潮中的技术积累",
            "probability": 0.6,
            "impact": 0.8
        }
    ],
    "risk_assessment": {
        "original_risk_score": 45,
        "alternative_risk_score": 65,
        "explanation": "..."
    },
    "overall_recommendation": "综合风险建议"
}"""

    async def execute(
        self,
        context: dict[str, Any],
    ) -> AsyncGenerator[AgentEvent, None]:
        scenario = context["scenario"]

        yield await self.emit_event(
            EventType.AGENT_START,
            AgentStatus.THINKING,
            "正在评估两条时间线的风险与机遇...",
        )

        user_prompt = f"""
用户场景：{scenario.choice_point}
替代选择：{scenario.alternative}
当前状态：{scenario.current_state}
时间跨度：{context.get('plan', {}).get('time_span', {})}
宏观经济：{context.get('macro_data', {})}
行业分析：{context.get('industry_data', {})}

请评估两条时间线的风险和隐藏机遇。
"""

        yield await self.emit_event(
            EventType.AGENT_PROGRESS,
            AgentStatus.ANALYZING,
            "正在计算风险概率和影响系数...",
        )

        messages = self._build_messages(self._build_system_prompt(), user_prompt)
        risk_data = await self.llm.chat_json(messages, temperature=0.3)

        yield await self.emit_event(
            EventType.AGENT_COMPLETE,
            AgentStatus.COMPLETE,
            "风险评估完成",
            data=risk_data,
        )
