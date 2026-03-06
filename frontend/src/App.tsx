import { useEffect, useMemo, useState } from "react";
import "./index.css";
import {
  getMetricsSummary,
  getPipelineLogs,
  getPipelineStatus,
  getMrrSeries,
  runPipeline,
  type PipelineStatus,
  type MrrPoint,
} from "./api";

function App() {
  const [status, setStatus] = useState<PipelineStatus>("idle");
  const [exitCode, setExitCode] = useState<number | undefined>(undefined);
  const [logs, setLogs] = useState<string[]>([]);
  const [metrics, setMetrics] = useState<Awaited<ReturnType<typeof getMetricsSummary>> | null>(null);
  const [mrrSeries, setMrrSeries] = useState<MrrPoint[]>([]);
  const [error, setError] = useState<string | null>(null);

  const isRunning = status === "running";
  const statusLabel = useMemo(() => {
    if (status === "idle") return "Idle";
    if (status === "running") return "Running";
    if (status === "succeeded") return "Succeeded";
    return `Failed${typeof exitCode === "number" ? ` (exit ${exitCode})` : ""}`;
  }, [status, exitCode]);

  async function refreshAll() {
    try {
      const [st, l, m, mrr] = await Promise.all([
        getPipelineStatus(),
        getPipelineLogs(200),
        getMetricsSummary().catch(() => null),
        getMrrSeries().catch(() => [] as MrrPoint[]),
      ]);
      setStatus(st.status);
      setExitCode(st.exit_code);
      setLogs(l.lines);
      if (m) setMetrics(m);
      setMrrSeries(mrr);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to refresh pipeline state");
    }
  }

  useEffect(() => {
    // Initial async load
    (async () => {
      await refreshAll();
    })();
    const id = setInterval(() => {
      void refreshAll();
    }, 2000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-inner">
          <div>
            <div className="app-title">SaaS Revenue &amp; Customer Intelligence Platform</div>
            <div className="app-subtitle">MRR • ARPU • LTV • Churn • Customer Health</div>
          </div>
          <span
            className={[
              "status-pill",
              status === "running"
                ? "status-running"
                : status === "succeeded"
                  ? "status-succeeded"
                  : status === "failed"
                    ? "status-failed"
                    : "",
            ].join(" ")}
          >
            Pipeline: {statusLabel}
          </span>
        </div>
      </header>

      <main className="app-main">
        <section>
          <div className="card">
            <h2 className="card-title">Run pipeline</h2>
            <p className="card-text">
              This triggers <code>scripts/run_all.py</code> on the backend, regenerating synthetic SaaS data, loading
              Postgres, building warehouse tables, and running data quality checks.
            </p>

            <div style={{ marginTop: "0.9rem", display: "flex", gap: "0.75rem" }}>
              <button
                disabled={isRunning}
                onClick={async () => {
                  try {
                    setError(null);
                    await runPipeline();
                    await refreshAll();
                  } catch (e) {
                    setError(e instanceof Error ? e.message : "Failed to start pipeline");
                  }
                }}
                className="btn btn-primary"
              >
                {isRunning ? "Running…" : "Run pipeline"}
              </button>
              <button onClick={() => void refreshAll()} className="btn btn-secondary">
                Refresh
              </button>
            </div>

            {error ? (
              <div
                style={{
                  marginTop: "0.75rem",
                  borderRadius: "0.75rem",
                  border: "1px solid rgba(248,113,113,0.6)",
                  backgroundColor: "rgba(127,29,29,0.35)",
                  padding: "0.5rem 0.75rem",
                  fontSize: "0.7rem",
                }}
              >
                {error}
              </div>
            ) : null}

            <div className="logs-container">
              <div className="logs-header">
                <span>Logs (tail)</span>
                <span>Last {logs.length} lines</span>
              </div>
              <pre className="logs-body">
                {logs.length ? logs.join("\n") : "No logs yet. Run the pipeline to see output here."}
              </pre>
            </div>
          </div>
        </section>

        <section>
          <div className="card">
            <h2 className="card-title">KPI snapshot</h2>
            <p className="card-text">
              Backed by the same Postgres warehouse the dbt models and dashboards use. Simple metrics for quick checks.
            </p>
            <div className="metrics-grid">
              <MetricCard label="Total customers" value={metrics?.total_customers} />
              <MetricCard label="Total subscriptions" value={metrics?.total_subscriptions} />
              <MetricCard label="Active subscriptions" value={metrics?.active_subscriptions} />
              <MetricCard
                label="Current MRR (synthetic)"
                value={metrics ? `$${metrics.current_mrr.toLocaleString()}` : undefined}
              />
            </div>
            <p className="helper-text">
              For richer analytics (ARPU, churn, LTV, customer health), see the dbt marts and business SQL in{" "}
              <code>sql/business_queries.sql</code>.
            </p>

            <div style={{ marginTop: "1rem" }}>
              <div className="metric-card-label" style={{ marginBottom: "0.35rem" }}>
                Monthly Recurring Revenue trend
              </div>
              <div className="mrr-table-wrapper">
                <table className="mrr-table">
                  <thead>
                    <tr>
                      <th>Month</th>
                      <th className="mrr-right">MRR</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mrrSeries.length === 0 ? (
                      <tr>
                        <td colSpan={2} className="mrr-empty">
                          No MRR data yet. Run the pipeline and dbt models to populate the <code>mrr</code> table.
                        </td>
                      </tr>
                    ) : (
                      mrrSeries.map((p) => (
                        <tr key={p.revenue_month}>
                          <td>{p.revenue_month}</td>
                          <td className="mrr-right">${p.mrr.toLocaleString()}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

type MetricCardProps = {
  label: string;
  value?: number | string;
};

function MetricCard({ label, value }: MetricCardProps) {
  return (
    <div className="card" style={{ padding: "0.9rem 1rem" }}>
      <div className="metric-card-label">{label}</div>
      <div className="metric-card-value">
        {value === undefined ? <span className="placeholder">—</span> : value}
      </div>
    </div>
  );
}

export default App;
