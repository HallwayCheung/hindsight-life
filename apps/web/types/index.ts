// Core types aligned with backend Pydantic models

export interface RegretScenario {
  choice_point: string;
  time_node: string;
  alternative: string;
  current_state: string;
  user_age_at_time?: number;
  user_education?: string;
  user_industry?: string;
  user_city?: string;
}

export interface SimulationRequest {
  scenario: RegretScenario;
  depth?: number;
  include_narrative?: boolean;
}

export interface SimulationResponse {
  simulation_id: string;
  status: string;
  stream_url: string;
}

// Agent Events
export type AgentName =
  | "planner"
  | "timeline"
  | "macro_economy"
  | "industry"
  | "risk"
  | "narrative";

export type AgentStatus =
  | "idle"
  | "thinking"
  | "analyzing"
  | "generating"
  | "complete"
  | "error";

export type EventType =
  | "agent_start"
  | "agent_progress"
  | "agent_complete"
  | "timeline_node"
  | "narrative_chunk"
  | "simulation_complete"
  | "simulation_error";

export interface AgentEvent {
  event_type: EventType;
  agent: AgentName;
  status: AgentStatus;
  message: string;
  data?: Record<string, unknown>;
  timestamp: string;
  event_id: string;
}

// Timeline
export interface TimelineNode {
  node_id: string;
  year: number;
  month?: number;
  title: string;
  description: string;
  event_type: string;
  probability: number;
  impact_score: number;
  financial_impact?: number;
  city?: string;
  industry?: string;
  tags: string[];
}

export interface TimelineBranch {
  branch_id: string;
  label: string;
  nodes: TimelineNode[];
  summary: string;
  overall_score: number;
}

export interface TimelineData {
  timeline_id: string;
  scenario_description: string;
  original_branch: TimelineBranch;
  alternative_branch: TimelineBranch;
  divergence_point: number;
  key_differences: string[];
}

// V3.0 Comparative Metrics
export interface MetricValue {
  reality: number;
  parallel: number;
  unit?: string;
  status?: [string, string]; // [reality_status, parallel_status]
  desc?: string;
}

export interface ComparativeMetrics {
  wealth_index: MetricValue;
  health_index: MetricValue;
  freedom_index: MetricValue;
  [key: string]: MetricValue;
}

// V3.0 Inventory Changes
export interface InventoryChanges {
  reality_gained: string[];
  parallel_gained: string[];
  parallel_lost: string[];
}

// V3.0 Timeline Node with butterfly effect
export interface ButterflyNode {
  year: number;
  event_reality: string;
  event_parallel: string;
  butterfly_effect: string;
}

// V3.0 Dashboard Data Shape
export interface V3DashboardData {
  soul_summary: string;
  comparative_metrics: ComparativeMetrics;
  inventory_changes: InventoryChanges;
  timeline_nodes: ButterflyNode[];
}

// V4.0 Emotional Metrics
export interface EmotionalMetric {
  reality: number;
  parallel: number;
  label: string;
}

export interface EmotionalMetrics {
  happiness_battery: EmotionalMetric;
  regret_index: EmotionalMetric;
  peace_of_mind: EmotionalMetric;
  [key: string]: EmotionalMetric;
}

// V4.0 Parallel Souvenir
export interface ParallelSouvenir {
  item_name: string;
  description: string;
  icon_type: string; // "ticket" | "letter" | "photo" | "key" | "ring"
}

// V4.0 Future Letter
export interface FutureLetter {
  greetings: string;
  content: string;
  signature: string;
}

// V4.0 Timeline Node
export interface V4TimelineNode {
  year: number;
  reality_snapshot: string;
  parallel_snapshot: string;
  divergence_point: string;
}

// V4.0 Dashboard Data Shape
export interface V4DashboardData {
  soul_summary: string;
  emotional_metrics: EmotionalMetrics;
  parallel_souvenir: ParallelSouvenir;
  future_letter: FutureLetter;
  timeline_nodes: V4TimelineNode[];
}

// Universe
export interface DimensionScore {
  dimension: string;
  original_score: number;
  alternative_score: number;
  description: string;
}

export interface UniverseState {
  universe_id: string;
  simulation_id: string;
  original_title: string;
  original_summary: string;
  original_financial_trajectory: number[];
  alternative_title: string;
  alternative_summary: string;
  alternative_financial_trajectory: number[];
  dimensions: DimensionScore[];
  key_insight: string;
  regret_score: number;
  growth_potential: number;
}

// Narrative
export interface NarrativeChapter {
  year: number;
  title: string;
  content: string;
}

export interface NarrativeBranch {
  title: string;
  opening: string;
  chapters: NarrativeChapter[];
  ending: string;
}

export interface NarrativeData {
  original_narrative: NarrativeBranch;
  alternative_narrative: NarrativeBranch;
  reflection: string;
  key_quote: string;
}

// Simulation state
export type SimulationPhase =
  | "idle"
  | "planning"
  | "timeline"
  | "analysis"
  | "risk"
  | "narrative"
  | "complete"
  | "error";

export interface SimulationState {
  simulationId: string | null;
  phase: SimulationPhase;
  events: AgentEvent[];
  timelineData: TimelineData | null;
  universeState: UniverseState | null;
  narrativeData: NarrativeData | null;
  error: string | null;
  isStreaming: boolean;
}
