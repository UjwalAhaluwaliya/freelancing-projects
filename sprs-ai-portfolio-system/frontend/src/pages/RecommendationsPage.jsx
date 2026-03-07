import { useEffect, useState } from "react";
import RecommendationPanel from "../components/RecommendationPanel";
import { getRecommendations } from "../services/portfolioService";

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError("");
      try {
        const response = await getRecommendations();
        setRecommendations(response.data || []);
      } catch (err) {
        setError(err.response?.data?.message || err.message || "Failed to fetch recommendations.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="page-grid">
      {loading ? <section className="card">Loading recommendations...</section> : null}
      {error ? <section className="card error">{error}</section> : null}
      {!loading && !error ? <RecommendationPanel recommendations={recommendations} /> : null}
    </div>
  );
}
