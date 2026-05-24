"use client";

import { useCallback, useRef } from "react";
import { SSEClient, type SSEOptions } from "@/lib/sse";
import type { AgentEvent, EventType } from "@/types";

interface UseSSEOptions {
  onEvent?: (event: AgentEvent) => void;
  onComplete?: () => void;
  onError?: (error: Event) => void;
  eventTypes?: EventType[];
}

export function useSSE() {
  const clientRef = useRef<SSEClient | null>(null);

  const connect = useCallback(
    (url: string, options: UseSSEOptions = {}) => {
      // Disconnect existing connection
      disconnect();

      const client = new SSEClient(url, {
        onEvent: options.onEvent,
        onComplete: options.onComplete,
        onError: options.onError,
        eventTypes: options.eventTypes,
      });

      client.connect();
      clientRef.current = client;
    },
    []
  );

  const disconnect = useCallback(() => {
    if (clientRef.current) {
      clientRef.current.disconnect();
      clientRef.current = null;
    }
  }, []);

  const isConnected = useCallback(() => {
    return clientRef.current?.isConnected() ?? false;
  }, []);

  return { connect, disconnect, isConnected };
}
