import { useEffect, useState } from "react";
import api from "../lib/api";
import { decodeToken, getToken } from "../lib/auth";

export default function EmployeeDashboard() {
  const [unread, setUnread] = useState(0);
  const [points, setPoints] = useState(0);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const payload = decodeToken(getToken() || "");
        const userId = payload?.user_id;
        const unreadResponse = await api.get("/notifications/unread-count");
        let pointsResponse = { data: { total_points: 0 } };
        if (userId) {
          pointsResponse = await api.get(`/achievements/total/${userId}`);
        }
        setUnread(unreadResponse.data?.unread_count || 0);
        setPoints(pointsResponse.data?.total_points || 0);
      } catch (err) {
        setError(err?.response?.data?.detail || "Employee dashboard load failed");
      }
    }
    load();
  }, []);

  const pointCap = 100;
  const pointPct = Math.min(100, Math.round((points / pointCap) * 100));

  return (
    <section>
      <h2>Employee Dashboard</h2>
      <p className="muted">Track notifications, leave activity and achievements.</p>
      {error ? <p className="error-text">{error}</p> : null}
      <div className="cards-grid">
        <article className="card metric-card">
          <p className="metric-label">Unread Notifications</p>
          <p className="metric-value">{unread}</p>
        </article>
        <article className="card metric-card">
          <p className="metric-label">Achievement Points</p>
          <p className="metric-value">{points}</p>
        </article>
      </div>
      <div className="split-grid">
        <article className="card">
          <h3>Recognition Meter</h3>
          <div className="ring-wrap">
            <div
              className="ring-chart"
              style={{
                background: `conic-gradient(var(--accent) ${Math.round(
                  (pointPct / 100) * 360,
                )}deg, rgba(249,115,22,0.16) 0deg)`,
              }}
            >
              <div className="ring-center">
                <strong>{points}</strong>
                <small>{pointPct}%</small>
              </div>
            </div>
          </div>
        </article>
        <article className="card">
          <h3>Activity Pulse</h3>
          <div className="hero-wave compact">
            <span />
            <span />
            <span />
            <span />
            <span />
            <span />
          </div>
        </article>
      </div>
    </section>
  );
}
