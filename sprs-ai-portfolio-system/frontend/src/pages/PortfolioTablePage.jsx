import { useEffect, useState } from "react";
import PortfolioTable from "../components/PortfolioTable";
import { getProjects } from "../services/portfolioService";

export default function PortfolioTablePage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError("");
      try {
        const response = await getProjects();
        setProjects(response.data || []);
      } catch (err) {
        setError(err.response?.data?.message || err.message || "Failed to fetch projects.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="page-grid">
      {loading ? <section className="card">Loading portfolio projects...</section> : null}
      {error ? <section className="card error">{error}</section> : null}
      {!loading && !error ? <PortfolioTable projects={projects} /> : null}
    </div>
  );
}
