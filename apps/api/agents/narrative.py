from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from agents.base import BaseAgent
from models.events import AgentEvent, AgentName, AgentStatus, EventType


class NarrativeAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentName.NARRATIVE)

    def _build_system_prompt(self) -> str:
        return """你是一个人生叙事大师，擅长将数据和推演转化为有温度的人生故事。

你的写作风格：
- 温暖、治愈、有人文关怀
- 像一封写给老朋友的信，真诚而克制
- 像独立杂志的卷首语，有文学感和哲思
- 像深夜电台的独白，温柔中带有力量

你需要为两条时间线各写一段叙事，让读者仿佛"重新经历了一次人生"。

结构：
1. 开场：时空感的营造（像电影开场）
2. 关键节点：每个重要时刻的场景化描写
3. 转折：命运分叉的那一刻
4. 结尾：带有哲思的回望

同时你需要生成以下额外数据：
- soul_summary：50-100字的核心洞察，温暖而深刻，像灵魂的低语
- emotional_metrics：三个情感维度的量化对比
- parallel_souvenir：来自平行宇宙的纪念品
- future_letter：平行宇宙的你写给现在你的一封信

输出格式（JSON）：
{
    "soul_summary": "你为了留住晚霞，错过了清晨的列车。平行宇宙里的你拥有了属于自己的车队，但副驾驶上，再也没有当年那个陪你躲雨的人。",
    "original_narrative": {
        "title": "留在成都的日子",
        "opening": "2018年的夏天...",
        "chapters": [
            {
                "year": 2018,
                "title": "选择",
                "content": "你站在人生的十字路口..."
            }
        ],
        "ending": "回望这些年..."
    },
    "alternative_narrative": {
        "title": "深圳的平行人生",
        "opening": "如果那年夏天...",
        "chapters": [...],
        "ending": "在另一个宇宙里..."
    },
    "reflection": "两条路的哲学思考",
    "key_quote": "一句点睛之笔",
    "emotional_metrics": {
        "happiness_battery": { "reality": 80, "parallel": 30, "label": "快乐电量" },
        "regret_index": { "reality": 20, "parallel": 65, "label": "遗憾指数" },
        "peace_of_mind": { "reality": 90, "parallel": 15, "label": "内心平静度" }
    },
    "parallel_souvenir": {
        "item_name": "一张褪色的头等舱机票",
        "description": "这是你在平行宇宙中频繁出差的证明。航程很远，但降落时没人接机。",
        "icon_type": "ticket"
    },
    "future_letter": {
        "greetings": "展信佳：",
        "content": "我是做出了那个选择的你。不要羡慕我，我现在的体检报告一塌糊涂。其实，我时常会偷偷溜到你的世界看你。照顾好现在的自己，那就是我们最好的结局。",
        "signature": "—— 另一个时空的你"
    },
    "timeline_nodes": [
        {
            "year": 2021,
            "reality_snapshot": "在老家按揭了一套小房子，周末和朋友去江边露营。",
            "parallel_snapshot": "拿到了人生第一个百万年薪，但确诊了中度抑郁状态。",
            "divergence_point": "得失守恒"
        }
    ]
}"""

    async def execute(
        self,
        context: dict[str, Any],
    ) -> AsyncGenerator[AgentEvent, None]:
        scenario = context["scenario"]
        timeline_data = context.get("timeline_data", {})
        risk_data = context.get("risk_data", {})

        yield await self.emit_event(
            EventType.AGENT_START,
            AgentStatus.THINKING,
            "正在为你编织两个平行宇宙的故事...",
        )

        user_prompt = f"""
用户的选择：
- 后悔点：{scenario.choice_point}
- 时间：{scenario.time_node}
- 替代选择：{scenario.alternative}
- 当前状态：{scenario.current_state}

时间线数据：
{timeline_data}

风险评估：
{risk_data}

请为两条时间线写出生动的叙事，让读者仿佛重新经历了一次人生。
写作风格：克制、深情、有宿命感、有科幻感。不要煽情，要有重量感。
"""

        yield await self.emit_event(
            EventType.AGENT_PROGRESS,
            AgentStatus.GENERATING,
            "正在生成平行宇宙记忆...",
        )

        messages = self._build_messages(self._build_system_prompt(), user_prompt)
        narrative_data = await self.llm.chat_json(messages, temperature=0.8, max_tokens=4000)

        # Stream narrative chunks
        for branch_key in ["original_narrative", "alternative_narrative"]:
            narrative = narrative_data.get(branch_key, {})
            yield await self.emit_event(
                EventType.NARRATIVE_CHUNK,
                AgentStatus.GENERATING,
                narrative.get("opening", "")[:100],
                data={"type": "opening", "branch": branch_key, "content": narrative.get("opening", "")},
            )

            for chapter in narrative.get("chapters", []):
                yield await self.emit_event(
                    EventType.NARRATIVE_CHUNK,
                    AgentStatus.GENERATING,
                    f"{chapter.get('year')}年：{chapter.get('title', '')}",
                    data={"type": "chapter", "branch": branch_key, "content": chapter.get("content", "")},
                )

            yield await self.emit_event(
                EventType.NARRATIVE_CHUNK,
                AgentStatus.GENERATING,
                narrative.get("ending", "")[:100],
                data={"type": "ending", "branch": branch_key, "content": narrative.get("ending", "")},
            )

        yield await self.emit_event(
            EventType.AGENT_COMPLETE,
            AgentStatus.COMPLETE,
            "平行宇宙叙事生成完成",
            data=narrative_data,
        )
