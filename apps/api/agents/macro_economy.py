from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from agents.base import BaseAgent
from models.events import AgentEvent, AgentName, AgentStatus, EventType


class MacroEconomyAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentName.MACRO_ECONOMY)

    def _build_system_prompt(self) -> str:
        return """你是一个宏观经济分析师。你的任务是分析推演时间跨度内的宏观经济环境。

你需要分析：
1. GDP 增长趋势
2. 行业周期
3. 就业市场
4. 房价走势
5. 薪资水平变化
6. 重大政策变化
7. 黑天鹅事件（如疫情、经济危机等）

输出格式（JSON）：
{
    "period": "2018-2024",
    "macro_trends": [
        {
            "year": 2018,
            "gdp_growth": 6.7,
            "industry_outlook": "positive",
            "key_events": ["中美贸易战开始"],
            "impact_on_user": "行业不确定性增加"
        }
    ],
    "housing_market": {"trend": "rising", "details": "..."},
    "salary_trends": {"tech": "+15%/year", "traditional": "+5%/year"},
    "black_swan_events": [
        {"year": 2020, "event": "新冠疫情", "impact": "远程办公兴起"}
    ],
    "overall_assessment": "整体经济环境评估"
}"""

    async def execute(
        self,
        context: dict[str, Any],
    ) -> AsyncGenerator[AgentEvent, None]:
        scenario = context["scenario"]
        plan = context.get("plan", {})
        time_span = plan.get("time_span", {})

        yield await self.emit_event(
            EventType.AGENT_START,
            AgentStatus.THINKING,
            f"正在分析 {time_span.get('start', 2018)}-{time_span.get('end', 2024)} 年宏观经济环境...",
        )

        user_prompt = f"""
推演时间跨度：{time_span}
用户所在行业：{scenario.user_industry or '未知'}
用户所在城市：{scenario.user_city or '未知'}
替代选择城市：从用户描述中推断

请分析该时间段的宏观经济环境。
"""

        yield await self.emit_event(
            EventType.AGENT_PROGRESS,
            AgentStatus.ANALYZING,
            "正在检索宏观经济数据和行业周期...",
        )

        messages = self._build_messages(self._build_system_prompt(), user_prompt)
        macro_data = await self.llm.chat_json(messages, temperature=0.3)

        yield await self.emit_event(
            EventType.AGENT_PROGRESS,
            AgentStatus.ANALYZING,
            f"已分析 {len(macro_data.get('macro_trends', []))} 年经济数据",
            data=macro_data,
        )

        yield await self.emit_event(
            EventType.AGENT_COMPLETE,
            AgentStatus.COMPLETE,
            "宏观经济分析完成",
            data=macro_data,
        )
