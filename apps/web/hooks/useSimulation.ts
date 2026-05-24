"use client";

import { useCallback } from "react";
import { useSSE } from "./useSSE";
import { useSimulationStore, getPhaseFromAgent } from "@/stores/simulation";
import { startSimulation, getSimulationStreamUrl } from "@/lib/api";
import type { SimulationRequest, AgentEvent, TimelineData, NarrativeData, UniverseState } from "@/types";

export function useSimulation() {
  const store = useSimulationStore();
  const { connect, disconnect, isConnected } = useSSE();

  const handleEvent = useCallback(
    (event: AgentEvent) => {
      store.addEvent(event);
      store.setPhase(getPhaseFromAgent(event.agent));

      // Extract data from completion events
      if (event.event_type === "agent_complete" && event.data) {
        switch (event.agent) {
          case "timeline":
            store.setTimelineData(event.data as unknown as TimelineData);
            break;
          case "narrative":
            store.setNarrativeData(event.data as unknown as NarrativeData);
            break;
        }
      }

      if (event.event_type === "simulation_complete" && event.data) {
        const data = event.data as Record<string, unknown>;
        if (data.universe_state) {
          store.setUniverseState(data.universe_state as UniverseState);
        }
        if (data.timeline_data) {
          store.setTimelineData(data.timeline_data as TimelineData);
        }
        if (data.narrative_data) {
          store.setNarrativeData(data.narrative_data as NarrativeData);
        }
        store.setPhase("complete");
        store.setStreaming(false);
      }

      if (event.event_type === "simulation_error") {
        store.setError(event.message || "Simulation failed");
        store.setStreaming(false);
      }
    },
    [store]
  );

  const start = useCallback(
    async (request: SimulationRequest) => {
      try {
        store.reset();
        store.setStreaming(true);

        // Create simulation
        const response = await startSimulation(request);
        store.setSimulationId(response.simulation_id);

        // Connect to SSE stream
        const streamUrl = getSimulationStreamUrl(response.simulation_id);
        connect(streamUrl, {
          onEvent: handleEvent,
          onComplete: () => {
            store.setPhase("complete");
            store.setStreaming(false);
          },
          onError: () => {
            store.setError("Connection lost");
            store.setStreaming(false);
          },
        });
      } catch (error) {
        store.setError(
          error instanceof Error ? error.message : "Failed to start simulation"
        );
        store.setStreaming(false);
      }
    },
    [store, connect, handleEvent]
  );

  const stop = useCallback(() => {
    disconnect();
    store.setStreaming(false);
  }, [disconnect, store]);

  return {
    ...store,
    start,
    stop,
    isConnected: isConnected(),
  };
}
