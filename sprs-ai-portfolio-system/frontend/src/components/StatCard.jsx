export default function StatCard({ title, value, subtitle }) {
  return (
    <section className="card stat-card">
      <p className="stat-title">{title}</p>
      <h3 className="stat-value">{value}</h3>
      {subtitle ? <p className="stat-subtitle">{subtitle}</p> : null}
    </section>
  );
}
