import { useEffect, useState } from "react";
import api from "../lib/api";

function Metric({ label, value }) {
  return (
    <article className="card metric-card">
      <p className="metric-label">{label}</p>
      <p className="metric-value">{value ?? "-"}</p>
    </article>
  );
}

export default function HrDashboard() {
  const [overview, setOverview] = useState(null);
  const [ats, setAts] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [overviewRes, atsRes] = await Promise.all([
          api.get("/dashboard/hr-overview"),
          api.get("/applications/dashboard"),
        ]);
        setOverview(overviewRes.data?.data || {});
        setAts(atsRes.data?.data || {});
      } catch (err) {
        setError(err?.response?.data?.detail || "Dashboard load failed");
      }
    }
    load();
  }, []);

  const pipeline = ats?.applications || {};
  const total = Math.max(1, pipeline.total || 1);
  const bars = [
    { key: "applied", label: "Applied", value: pipeline.applied || 0 },
    { key: "screening", label: "Screening", value: pipeline.screening || 0 },
    { key: "interview", label: "Interview", value: pipeline.interview || 0 },
    { key: "offer", label: "Offer", value: pipeline.offer || 0 },
    { key: "hired", label: "Hired", value: pipeline.hired || 0 },
  ];

  return (
    <section>
      <h2>HR Control Center</h2>
      <p className="muted">Hiring velocity, talent pipeline, and workforce status.</p>
      {error ? <p className="error-text">{error}</p> : null}
      <div className="cards-grid">
        <Metric label="Employees" value={overview?.employees} />
        <Metric label="Candidates" value={overview?.candidates} />
        <Metric label="Active Jobs" value={overview?.active_jobs} />
        <Metric label="Hired" value={pipeline.hired} />
      </div>
      <div className="split-grid">
        <article className="card">
          <h3>Pipeline Distribution</h3>
          <div className="chart-bars">
            {bars.map((bar) => (
              <div key={bar.key} className="bar-row">
                <span>{bar.label}</span>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{ width: `${Math.round((bar.value / total) * 100)}%` }}
                  />
                </div>
                <b>{bar.value}</b>
              </div>
            ))}
          </div>
        </article>
        <article className="card">
          <h3>Hiring Pulse</h3>
          <div className="ring-wrap">
            <div
              className="ring-chart"
              style={{
                background: `conic-gradient(var(--primary) ${
                  Math.round(((pipeline.hired || 0) / total) * 360)
                }deg, rgba(13,148,136,0.16) 0deg)`,
              }}
            >
              <div className="ring-center">
                <strong>{pipeline.hired || 0}</strong>
                <small>Hired</small>
              </div>
            </div>
          </div>
        </article>
      </div>
    </section>
  );
}
