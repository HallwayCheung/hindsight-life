import type {
  TimelineData,
  UniverseState,
  NarrativeData,
  V4DashboardData,
  EmotionalMetrics,
  ParallelSouvenir,
  FutureLetter,
  V4TimelineNode,
} from "@/types";

const DEFAULT_EMOTIONAL_METRICS: EmotionalMetrics = {
  happiness_battery: { reality: 70, parallel: 40, label: "快乐电量" },
  regret_index: { reality: 30, parallel: 60, label: "遗憾指数" },
  peace_of_mind: { reality: 75, parallel: 25, label: "内心平静度" },
};

const DEFAULT_SOUVENIR: ParallelSouvenir = {
  item_name: "一张未寄出的明信片",
  description: "上面写着你想说却没说出口的话。",
  icon_type: "letter",
};

const DEFAULT_LETTER: FutureLetter = {
  greetings: "展信佳：",
  content:
    "我是做出了那个选择的你。不要羡慕我，每条路都有自己的风景。照顾好现在的自己，那就是我们最好的结局。",
  signature: "—— 另一个时空的你",
};

// Helper to access V4 fields that may be on the universe/narrative object
function getV4Field<T>(obj: unknown, key: string, fallback: T): T {
  const rec = obj as unknown as Record<string, unknown>;
  return (rec?.[key] as T) ?? fallback;
}

export function adaptSimulationData(
  timeline: TimelineData,
  universe: UniverseState,
  narrative?: NarrativeData | null
): V4DashboardData {
  const universeExt = universe as unknown as Record<string, unknown>;
  const narrativeExt = narrative as unknown as Record<string, unknown>;

  // Soul summary
  const soulSummary =
    (universeExt?.soul_summary as string) ||
    narrative?.reflection ||
    universe.key_insight ||
    "命运的天平从未倾斜。";

  // Emotional metrics — prefer backend, fall back to defaults
  const emotionalMetrics: EmotionalMetrics =
    (universeExt?.emotional_metrics as EmotionalMetrics) ||
    (narrativeExt?.emotional_metrics as EmotionalMetrics) ||
    DEFAULT_EMOTIONAL_METRICS;

  // Parallel souvenir
  const souvenir: ParallelSouvenir =
    (universeExt?.parallel_souvenir as ParallelSouvenir) ||
    (narrativeExt?.parallel_souvenir as ParallelSouvenir) ||
    DEFAULT_SOUVENIR;

  // Future letter
  const letter: FutureLetter =
    (universeExt?.future_letter as FutureLetter) ||
    (narrativeExt?.future_letter as FutureLetter) ||
    DEFAULT_LETTER;

  // Timeline nodes — prefer backend, fall back to building from branches
  let timelineNodes: V4TimelineNode[];
  if (universeExt?.timeline_nodes) {
    timelineNodes = universeExt.timeline_nodes as V4TimelineNode[];
  } else {
    const origNodes = timeline.original_branch.nodes;
    const altNodes = timeline.alternative_branch.nodes;
    const nodeCount = Math.max(origNodes.length, altNodes.length);
    timelineNodes = Array.from({ length: nodeCount }, (_, i) => {
      const orig = origNodes[i];
      const alt = altNodes[i];
      return {
        year: orig?.year ?? alt?.year ?? 2020,
        reality_snapshot: orig?.description ?? "—",
        parallel_snapshot: alt?.description ?? "—",
        divergence_point: "",
      };
    });
  }

  return {
    soul_summary: soulSummary,
    emotional_metrics: emotionalMetrics,
    parallel_souvenir: souvenir,
    future_letter: letter,
    timeline_nodes: timelineNodes,
  };
}
