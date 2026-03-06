const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type PipelineStatus = "idle" | "running" | "succeeded" | "failed";

export async function runPipeline() {
  const res = await fetch(`${API_BASE}/pipeline/run`, { method: "POST" });
  if (!res.ok) {
    throw new Error(`Failed to start pipeline (status ${res.status})`);
  }
  return (await res.json()) as { status: string };
}

export async function getPipelineStatus() {
  const res = await fetch(`${API_BASE}/pipeline/status`);
  if (!res.ok) {
    throw new Error(`Failed to get status (status ${res.status})`);
  }
  return (await res.json()) as { status: PipelineStatus; exit_code?: number };
}

export async function getPipelineLogs(lines = 200) {
  const res = await fetch(`${API_BASE}/pipeline/logs?lines=${lines}`);
  if (!res.ok) {
    throw new Error(`Failed to get logs (status ${res.status})`);
  }
  return (await res.json()) as { lines: string[] };
}

export async function getMetricsSummary() {
  const res = await fetch(`${API_BASE}/metrics/summary`);
  if (!res.ok) {
    throw new Error(`Failed to get metrics (status ${res.status})`);
  }
  return (await res.json()) as {
    total_customers: number;
    total_subscriptions: number;
    active_subscriptions: number;
    current_mrr: number;
  };
}

export type MrrPoint = {
  revenue_month: string;
  mrr: number;
};

export async function getMrrSeries() {
  const res = await fetch(`${API_BASE}/metrics/mrr`);
  if (!res.ok) {
    throw new Error(`Failed to get MRR series (status ${res.status})`);
  }
  const data = (await res.json()) as { points: MrrPoint[] };
  return data.points;
}


