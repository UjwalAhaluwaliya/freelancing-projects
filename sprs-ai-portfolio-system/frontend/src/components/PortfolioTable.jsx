export default function PortfolioTable({ projects }) {
  return (
    <div className="card table-wrap">
      <h2>Portfolio Projects</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Budget</th>
            <th>ROI</th>
            <th>Risk</th>
            <th>Alignment</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project) => (
            <tr key={project._id}>
              <td>{project.project_name}</td>
              <td>{project.budget?.toLocaleString?.() || project.budget}</td>
              <td>{project.expected_roi}</td>
              <td>{project.risk_level}</td>
              <td>{project.strategic_alignment_score}</td>
              <td><span className="pill">{project.status}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
