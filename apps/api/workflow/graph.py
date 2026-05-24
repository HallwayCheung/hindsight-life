from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from agents.planner import PlannerAgent
from agents.timeline import TimelineAgent
from agents.macro_economy import MacroEconomyAgent
from agents.industry import IndustryAgent
from agents.risk import RiskAgent
from agents.narrative import NarrativeAgent
from models.events import AgentEvent, AgentName, AgentStatus, EventType
from models.scenario import RegretScenario
from core.logging import get_logger
from workflow.state import SimulationState

logger = get_logger("workflow")


class SimulationWorkflow:
    def __init__(self):
        self.planner = PlannerAgent()
        self.timeline = TimelineAgent()
        self.macro_economy = MacroEconomyAgent()
        self.industry = IndustryAgent()
        self.risk = RiskAgent()
        self.narrative = NarrativeAgent()

    async def run(
        self,
        scenario: RegretScenario,
        simulation_id: str | None = None,
    ) -> AsyncGenerator[AgentEvent, None]:
        state = SimulationState(
            scenario=scenario,
            simulation_id=simulation_id or SimulationState().simulation_id,
        )

        logger.info(f"Starting simulation {state.simulation_id}")

        # Phase 1: Planning
        state.current_agent = "planner"
        async for event in self.planner.execute({"scenario": scenario}):
            yield event
            if event.event_type == EventType.AGENT_COMPLETE and event.data:
                state.plan = event.data

        # Phase 2: Timeline Generation
        state.current_agent = "timeline"
        context = {"scenario": scenario, "plan": state.plan}
        async for event in self.timeline.execute(context):
            yield event
            if event.event_type == EventType.AGENT_COMPLETE and event.data:
                state.timeline_data = event.data

        # Phase 3: Macro Economy Analysis (parallel with Industry)
        state.current_agent = "macro_economy"
        context = {"scenario": scenario, "plan": state.plan}

        # Run macro and industry in parallel
        macro_events = []
        industry_events = []

        async def collect_macro():
            async for event in self.macro_economy.execute(context):
                macro_events.append(event)

        async def collect_industry():
            async for event in self.industry.execute(context):
                industry_events.append(event)

        await asyncio.gather(collect_macro(), collect_industry())

        # Yield macro events, then industry events
        for event in macro_events:
            yield event
            if event.event_type == EventType.AGENT_COMPLETE and event.data:
                state.macro_data = event.data

        for event in industry_events:
            yield event
            if event.event_type == EventType.AGENT_COMPLETE and event.data:
                state.industry_data = event.data

        # Phase 4: Risk Assessment
        state.current_agent = "risk"
        context = {
            "scenario": scenario,
            "plan": state.plan,
            "timeline_data": state.timeline_data,
            "macro_data": state.macro_data,
            "industry_data": state.industry_data,
        }
        async for event in self.risk.execute(context):
            yield event
            if event.event_type == EventType.AGENT_COMPLETE and event.data:
                state.risk_data = event.data

        # Phase 5: Narrative Generation
        state.current_agent = "narrative"
        context = {
            "scenario": scenario,
            "plan": state.plan,
            "timeline_data": state.timeline_data,
            "risk_data": state.risk_data,
        }
        async for event in self.narrative.execute(context):
            yield event
            if event.event_type == EventType.AGENT_COMPLETE and event.data:
                state.narrative_data = event.data

        # Build final universe state
        state.universe_state = self._build_universe_state(state)

        # Final completion event
        yield AgentEvent(
            event_type=EventType.SIMULATION_COMPLETE,
            agent=AgentName(state.current_agent) if state.current_agent else AgentName.PLANNER,
            status=AgentStatus.COMPLETE,
            message="推演完成",
            data={
                "simulation_id": state.simulation_id,
                "universe_state": state.universe_state,
                "timeline_data": state.timeline_data,
                "narrative_data": state.narrative_data,
            },
        )

        logger.info(f"Simulation {state.simulation_id} completed")

    def _build_universe_state(self, state: SimulationState) -> dict[str, Any]:
        dimensions = self._calculate_dimensions(state)
        narrative = state.narrative_data or {}
        timeline = state.timeline_data or {}

        # Build V4 timeline_nodes
        orig_nodes = timeline.get("original_branch", {}).get("nodes", [])
        alt_nodes = timeline.get("alternative_branch", {}).get("nodes", [])

        timeline_nodes = []
        for i in range(max(len(orig_nodes), len(alt_nodes))):
            orig = orig_nodes[i] if i < len(orig_nodes) else {}
            alt = alt_nodes[i] if i < len(alt_nodes) else {}
            year = orig.get("year", alt.get("year", 2020))
            timeline_nodes.append({
                "year": year,
                "reality_snapshot": orig.get("description", ""),
                "parallel_snapshot": alt.get("description", ""),
                "divergence_point": "",
            })

        return {
            "universe_id": state.simulation_id,
            "simulation_id": state.simulation_id,
            "original_title": timeline.get("original_branch", {}).get("label", "原始时间线"),
            "original_summary": timeline.get("original_branch", {}).get("summary", ""),
            "alternative_title": timeline.get("alternative_branch", {}).get("label", "平行时间线"),
            "alternative_summary": timeline.get("alternative_branch", {}).get("summary", ""),
            "dimensions": dimensions,
            "key_insight": narrative.get("reflection", ""),
            "regret_score": self._calculate_regret_score(state),
            "growth_potential": self._calculate_growth_potential(state),
            # V4.0 fields
            "soul_summary": narrative.get("soul_summary", narrative.get("reflection", "")),
            "emotional_metrics": narrative.get("emotional_metrics", {}),
            "parallel_souvenir": narrative.get("parallel_souvenir", {}),
            "future_letter": narrative.get("future_letter", {}),
            "timeline_nodes": timeline_nodes,
        }

    def _calculate_dimensions(self, state: SimulationState) -> list[dict[str, Any]]:
        # Extract from risk data
        risk = state.risk_data
        original_risk = risk.get("risk_assessment", {}).get("original_risk_score", 50)
        alternative_risk = risk.get("risk_assessment", {}).get("alternative_risk_score", 50)

        return [
            {
                "dimension": "职业发展",
                "original_score": max(0, 100 - original_risk),
                "alternative_score": max(0, 100 - alternative_risk),
                "description": "职业成长空间",
            },
            {
                "dimension": "财务状况",
                "original_score": 50,
                "alternative_score": 70,
                "description": "收入和财富积累",
            },
            {
                "dimension": "生活平衡",
                "original_score": 70,
                "alternative_score": 50,
                "description": "工作与生活平衡",
            },
            {
                "dimension": "成长空间",
                "original_score": 40,
                "alternative_score": 75,
                "description": "个人成长和学习机会",
            },
            {
                "dimension": "稳定性",
                "original_score": 80,
                "alternative_score": 55,
                "description": "生活和职业稳定性",
            },
        ]

    def _calculate_regret_score(self, state: SimulationState) -> float:
        risk = state.risk_data
        original_risk = risk.get("risk_assessment", {}).get("original_risk_score", 50)
        alternative_risk = risk.get("risk_assessment", {}).get("alternative_risk_score", 50)
        # Higher risk in original = more regret about not switching
        return min(100, max(0, (alternative_risk - original_risk) + 50))

    def _calculate_growth_potential(self, state: SimulationState) -> float:
        risk = state.risk_data
        opportunities = risk.get("hidden_opportunities", [])
        if not opportunities:
            return 50.0
        avg_impact = sum(o.get("impact", 0.5) for o in opportunities) / len(opportunities)
        return min(100, max(0, avg_impact * 100))
