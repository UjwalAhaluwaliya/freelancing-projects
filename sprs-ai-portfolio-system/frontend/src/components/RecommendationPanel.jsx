export default function RecommendationPanel({ recommendations }) {
  return (
    <div className="card recommendation-grid glow-panel">
      <div className="title-row">
        <h2>AI Recommendations</h2>
        <span className="chip">Live Intelligence</span>
      </div>
      <div className="recommendation-list">
        {recommendations.length === 0 ? <p>No recommendations available yet.</p> : null}
        {recommendations.map((rec, index) => (
          <article key={rec._id || `${rec.analysis_id}-${rec.project_id}-${index}`} className="recommendation-item">
            <div>
              <p className="recommendation-title">{rec.project_name || "Unknown Project"}</p>
              <p className="recommendation-id">ID: {rec.project_id}</p>
              <p className="recommendation-meta">
                Confidence: {Math.round((rec.confidence_score || 0) * 100)}% | Priority: {rec.priority_rank}
              </p>
            </div>
            <span className={`label ${String(rec.decision || "").toLowerCase()}`}>{rec.decision}</span>
          </article>
        ))}
      </div>
    </div>
  );
}
