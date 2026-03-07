import { useEffect, useState } from "react";
import {
  ClusterChart,
  PriorityChart,
  RiskDistributionChart,
  RoiDistributionChart
} from "../components/AnalyticsCharts";
import { analyzePortfolio, getProjects } from "../services/portfolioService";
import {
  buildClusterPoints,
  buildPriorityScores,
  buildRiskDistribution,
  buildRoiBuckets
} from "../utils/chartData";

export default function AnalyticsPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [running, setRunning] = useState(false);
  const [message, setMessage] = useState("");

  async function loadProjects() {
    setLoading(true);
    setError("");
    try {
      const response = await getProjects();
      setProjects(response.data || []);
    } catch (err) {
      setError(err.response?.data?.message || err.message || "Failed to load projects.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProjects();
  }, []);

  async function runAnalysis() {
    setRunning(true);
    setMessage("");
    setError("");
    try {
      await analyzePortfolio({ analysis_name: "Frontend Triggered Analysis" });
      setMessage("Analysis completed. Recommendations updated.");
      await loadProjects();
    } catch (err) {
      setError(err.response?.data?.message || err.message || "Analysis failed.");
    } finally {
      setRunning(false);
    }
  }

  const roiData = buildRoiBuckets(projects);
  const riskData = buildRiskDistribution(projects);
  const priorityData = buildPriorityScores(projects);
  const clusterData = buildClusterPoints(projects);

  return (
    <div className="page-grid">
      <section className="card actions-row">
        <h2>Analytics Dashboard</h2>
        <button className="btn" onClick={runAnalysis} disabled={running || loading}>
          {running ? "Running..." : "Run Portfolio Analysis"}
        </button>
        {message ? <p className="notice">{message}</p> : null}
      </section>
      {loading ? <section className="card">Loading analytics data...</section> : null}
      {error ? <section className="card error">{error}</section> : null}
      {!loading && !error ? (
        <div className="chart-grid">
          <RoiDistributionChart data={roiData} />
          <RiskDistributionChart data={riskData} />
          <PriorityChart data={priorityData} />
          <ClusterChart data={clusterData} />
        </div>
      ) : null}
    </div>
  );
}
