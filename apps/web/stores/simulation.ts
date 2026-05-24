"use client";

import { create } from "zustand";
import type {
  AgentEvent,
  SimulationPhase,
  SimulationState,
  TimelineData,
  UniverseState,
  NarrativeData,
} from "@/types";

interface SimulationStore extends SimulationState {
  // Actions
  setSimulationId: (id: string) => void;
  setPhase: (phase: SimulationPhase) => void;
  addEvent: (event: AgentEvent) => void;
  setTimelineData: (data: TimelineData) => void;
  setUniverseState: (state: UniverseState) => void;
  setNarrativeData: (data: NarrativeData) => void;
  setError: (error: string | null) => void;
  setStreaming: (isStreaming: boolean) => void;
  reset: () => void;
}

const initialState: SimulationState = {
  simulationId: null,
  phase: "idle",
  events: [],
  timelineData: null,
  universeState: null,
  narrativeData: null,
  error: null,
  isStreaming: false,
};

export const useSimulationStore = create<SimulationStore>((set) => ({
  ...initialState,

  setSimulationId: (id) => set({ simulationId: id }),

  setPhase: (phase) => set({ phase }),

  addEvent: (event) =>
    set((state) => ({
      events: [...state.events, event],
    })),

  setTimelineData: (data) => set({ timelineData: data }),

  setUniverseState: (universeState) => set({ universeState }),

  setNarrativeData: (data) => set({ narrativeData: data }),

  setError: (error) => set({ error, phase: error ? "error" : "idle" }),

  setStreaming: (isStreaming) => set({ isStreaming }),

  reset: () => set(initialState),
}));

// Helper to determine phase from agent events
export function getPhaseFromAgent(agent: string): SimulationPhase {
  switch (agent) {
    case "planner":
      return "planning";
    case "timeline":
      return "timeline";
    case "macro_economy":
    case "industry":
      return "analysis";
    case "risk":
      return "risk";
    case "narrative":
      return "narrative";
    default:
      return "idle";
  }
}
