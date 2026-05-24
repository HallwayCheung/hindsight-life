from typing import Optional

from fastapi import HTTPException, status


class SimulationNotFoundError(HTTPException):
    def __init__(self, simulation_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation '{simulation_id}' not found",
        )


class SimulationTimeoutError(HTTPException):
    def __init__(self, simulation_id: str):
        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Simulation '{simulation_id}' timed out",
        )


class AgentExecutionError(Exception):
    def __init__(self, agent_name: str, message: str):
        self.agent_name = agent_name
        self.message = message
        super().__init__(f"Agent '{agent_name}' failed: {message}")


class DashScopeAPIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(f"DashScope API error: {message}")


class InvalidScenarioError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid scenario: {detail}",
        )
