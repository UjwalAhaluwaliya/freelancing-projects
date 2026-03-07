import { useEffect, useState } from "react";
import StatCard from "../components/StatCard";
import RecommendationPanel from "../components/RecommendationPanel";
import { getDashboardMetrics, getRecommendations } from "../services/portfolioService";

export default function DashboardPage() {
  const [metrics, setMetrics] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError("");
      try {
        const [metricsResponse, recResponse] = await Promise.all([
          getDashboardMetrics(),
          getRecommendations()
        ]);
        setMetrics(metricsResponse.data || {});
        setRecommendations((recResponse.data || []).slice(0, 5));
      } catch (err) {
        setError(err.response?.data?.message || err.message || "Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const distribution = metrics?.recommendation_distribution || {};

  return (
    <div className="page-grid">
      <h2>Dashboard</h2>
      {loading ? <section className="card">Loading dashboard data...</section> : null}
      {error ? <section className="card error">{error}</section> : null}
      {!loading && !error ? (
        <>
          <section className="stats-grid">
            <StatCard title="Total Projects" value={metrics?.total_projects ?? 0} />
            <StatCard title="Active Projects" value={metrics?.active_projects ?? 0} />
            <StatCard title="Average Budget" value={metrics?.average_project_budget ?? 0} />
            <StatCard title="Recommendations" value={Object.values(distribution).reduce((a, b) => a + b, 0)} />
          </section>
          <section className="card">
            <h3>Decision Distribution</h3>
            <div className="inline-tags">
              {Object.keys(distribution).length === 0 ? <p>No recommendations yet.</p> : null}
              {Object.entries(distribution).map(([key, count]) => (
                <span key={key} className="pill">{key}: {count}</span>
              ))}
            </div>
          </section>
          <RecommendationPanel recommendations={recommendations} />
        </>
      ) : null}
    </div>
  );
}
