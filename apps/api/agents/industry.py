from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from agents.base import BaseAgent
from models.events import AgentEvent, AgentName, AgentStatus, EventType


class IndustryAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentName.INDUSTRY)

    def _build_system_prompt(self) -> str:
        return """你是一个行业分析师。你的任务是分析用户所在行业和目标行业的发展趋势。

你需要分析：
1. 行业增长趋势
2. 技术变革影响
3. 人才供需变化
4. 薪资水平变化
5. 行业风口和衰退信号
6. AI/互联网对该行业的影响

输出格式（JSON）：
{
    "original_industry": {
        "name": "传统行业",
        "trend": "stable",
        "growth_rate": "3%",
        "key_changes": ["数字化转型"],
        "risk_level": "medium"
    },
    "target_industry": {
        "name": "互联网/科技",
        "trend": "volatile",
        "growth_rate": "15%",
        "key_changes": ["AI革命"],
        "risk_level": "high"
    },
    "industry_comparison": {
        "salary_gap": "50%",
        "growth_gap": "10%",
        "stability_gap": "传统行业更稳定"
    },
    "future_outlook": "行业未来展望"
}"""

    async def execute(
        self,
        context: dict[str, Any],
    ) -> AsyncGenerator[AgentEvent, None]:
        scenario = context["scenario"]

        yield await self.emit_event(
            EventType.AGENT_START,
            AgentStatus.THINKING,
            f"正在分析行业发展趋势...",
        )

        user_prompt = f"""
用户当前行业：{scenario.user_industry or '未知'}
用户后悔选择：{scenario.choice_point}
替代选择：{scenario.alternative}
时间跨度：{context.get('plan', {}).get('time_span', {})}

请分析两个行业的发展对比。
"""

        yield await self.emit_event(
            EventType.AGENT_PROGRESS,
            AgentStatus.ANALYZING,
            "正在分析行业数据和人才市场...",
        )

        messages = self._build_messages(self._build_system_prompt(), user_prompt)
        industry_data = await self.llm.chat_json(messages, temperature=0.3)

        yield await self.emit_event(
            EventType.AGENT_COMPLETE,
            AgentStatus.COMPLETE,
            "行业分析完成",
            data=industry_data,
        )
