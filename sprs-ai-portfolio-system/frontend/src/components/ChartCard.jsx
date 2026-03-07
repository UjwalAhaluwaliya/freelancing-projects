export default function ChartCard({ title, children }) {
  return (
    <section className="card chart-card">
      <h3>{title}</h3>
      <div className="chart-wrap">{children}</div>
    </section>
  );
}
