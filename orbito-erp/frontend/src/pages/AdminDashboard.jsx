import { useEffect, useState } from "react";
import api from "../lib/api";

export default function AdminDashboard() {
  const [profiles, setProfiles] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const response = await api.get("/profiles");
        setProfiles(response.data?.data || []);
      } catch (err) {
        setError(err?.response?.data?.detail || "Admin dashboard load failed");
      }
    }
    load();
  }, []);

  const roleCount = profiles.reduce((acc, item) => {
    const role = item.role || "unknown";
    acc[role] = (acc[role] || 0) + 1;
    return acc;
  }, {});

  const total = Math.max(1, profiles.length);

  return (
    <section>
      <h2>Admin Overview</h2>
      <p className="muted">System users and role distribution snapshot.</p>
      {error ? <p className="error-text">{error}</p> : null}
      <div className="cards-grid">
        <article className="card metric-card">
          <p className="metric-label">Total Profiles</p>
          <p className="metric-value">{profiles.length}</p>
        </article>
        <article className="card metric-card">
          <p className="metric-label">Admins</p>
          <p className="metric-value">{roleCount.admin || 0}</p>
        </article>
        <article className="card metric-card">
          <p className="metric-label">HR</p>
          <p className="metric-value">{roleCount.hr || 0}</p>
        </article>
        <article className="card metric-card">
          <p className="metric-label">Employees</p>
          <p className="metric-value">{roleCount.employee || 0}</p>
        </article>
      </div>
      <article className="card">
        <h3>Role Balance</h3>
        <div className="chart-bars">
          {["admin", "hr", "employee"].map((role) => (
            <div key={role} className="bar-row">
              <span>{role.toUpperCase()}</span>
              <div className="bar-track">
                <div
                  className="bar-fill"
                  style={{ width: `${Math.round(((roleCount[role] || 0) / total) * 100)}%` }}
                />
              </div>
              <b>{roleCount[role] || 0}</b>
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}
