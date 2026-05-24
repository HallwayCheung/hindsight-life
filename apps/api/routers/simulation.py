from __future__ import annotations

import asyncio
import json
import uuid
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from models.scenario import SimulationRequest, RegretScenario
from models.events import AgentEvent, EventType
from workflow.graph import SimulationWorkflow
from core.logging import get_logger

logger = get_logger("simulation_router")

router = APIRouter(prefix="/simulation", tags=["simulation"])


@dataclass
class SimulationRecord:
    scenario: RegretScenario
    events: list[AgentEvent] = field(default_factory=list)


# In-memory store (Phase 1, replace with Redis later)
active_simulations: dict[str, SimulationRecord] = {}


@router.post("/start")
async def start_simulation(request: SimulationRequest):
    simulation_id = uuid.uuid4().hex[:16]
    active_simulations[simulation_id] = SimulationRecord(scenario=request.scenario)

    logger.info(f"Simulation {simulation_id} created: {request.scenario.choice_point[:30]}")

    return {
        "simulation_id": simulation_id,
        "status": "created",
        "stream_url": f"/api/simulation/{simulation_id}/stream",
    }


@router.get("/{simulation_id}/stream")
async def stream_simulation(simulation_id: str):
    record = active_simulations.get(simulation_id)
    if not record:
        return {"error": "Simulation not found"}

    scenario = record.scenario

    async def event_generator() -> AsyncGenerator[dict, None]:
        workflow = SimulationWorkflow()

        try:
            async for event in workflow.run(scenario, simulation_id):
                record.events.append(event)

                yield {
                    "event": event.event_type.value,
                    "data": event.model_dump_json(),
                }

                await asyncio.sleep(0.05)

        except Exception as e:
            logger.error(f"Simulation {simulation_id} failed: {e}")
            yield {
                "event": EventType.SIMULATION_ERROR.value,
                "data": json.dumps({"error": str(e)}),
            }

    return EventSourceResponse(event_generator())


@router.get("/{simulation_id}/events")
async def get_simulation_events(simulation_id: str):
    record = active_simulations.get(simulation_id)
    if not record:
        return {"error": "Simulation not found"}

    return {
        "simulation_id": simulation_id,
        "event_count": len(record.events),
        "events": [e.model_dump() for e in record.events],
    }
