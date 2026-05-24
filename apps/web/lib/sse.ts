import type { AgentEvent, EventType } from "@/types";

type EventHandler = (event: AgentEvent) => void;
type ErrorHandler = (error: Event) => void;

export interface SSEOptions {
  onEvent?: EventHandler;
  onComplete?: () => void;
  onError?: ErrorHandler;
  eventTypes?: EventType[];
}

export class SSEClient {
  private eventSource: EventSource | null = null;
  private url: string;
  private options: SSEOptions;

  constructor(url: string, options: SSEOptions = {}) {
    this.url = url;
    this.options = options;
  }

  connect(): void {
    this.disconnect();

    this.eventSource = new EventSource(this.url);

    // Listen for specific event types or all events
    const eventTypes = this.options.eventTypes || [
      "agent_start",
      "agent_progress",
      "agent_complete",
      "timeline_node",
      "narrative_chunk",
      "simulation_complete",
      "simulation_error",
    ];

    for (const eventType of eventTypes) {
      this.eventSource.addEventListener(eventType, (event: MessageEvent) => {
        try {
          const data: AgentEvent = JSON.parse(event.data);
          this.options.onEvent?.(data);

          if (eventType === "simulation_complete") {
            this.options.onComplete?.();
            this.disconnect();
          }

          if (eventType === "simulation_error") {
            this.disconnect();
          }
        } catch (e) {
          console.error(`Failed to parse SSE event: ${e}`);
        }
      });
    }

    this.eventSource.onerror = (error) => {
      this.options.onError?.(error);
      this.disconnect();
    };
  }

  disconnect(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }

  isConnected(): boolean {
    return this.eventSource?.readyState === EventSource.OPEN;
  }
}
