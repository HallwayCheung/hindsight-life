import type {
  SimulationRequest,
  SimulationResponse,
  AgentEvent,
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function startSimulation(
  request: SimulationRequest
): Promise<SimulationResponse> {
  const response = await fetch(`${API_BASE}/simulation/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Failed to start simulation: ${response.statusText}`);
  }

  return response.json();
}

export async function getSimulationEvents(
  simulationId: string
): Promise<{ simulation_id: string; event_count: number; events: AgentEvent[] }> {
  const response = await fetch(`${API_BASE}/simulation/${simulationId}/events`);

  if (!response.ok) {
    throw new Error(`Failed to get events: ${response.statusText}`);
  }

  return response.json();
}

export function getSimulationStreamUrl(simulationId: string): string {
  return `${API_BASE}/simulation/${simulationId}/stream`;
}
