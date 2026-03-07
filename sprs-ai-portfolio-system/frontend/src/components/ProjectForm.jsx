import { useState } from "react";

const defaultProject = {
  project_name: "",
  description: "",
  budget: "",
  expected_roi: "",
  risk_level: "medium",
  team_size: "",
  technology_stack: "",
  duration: "",
  strategic_alignment_score: "",
  status: "proposed"
};

export default function ProjectForm({ onSubmit, loading }) {
  const [form, setForm] = useState(defaultProject);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    const payload = {
      ...form,
      budget: Number(form.budget),
      expected_roi: Number(form.expected_roi),
      team_size: Number(form.team_size),
      duration: Number(form.duration),
      strategic_alignment_score: Number(form.strategic_alignment_score),
      technology_stack: form.technology_stack.split(",").map((item) => item.trim()).filter(Boolean)
    };
    await onSubmit(payload);
    setForm(defaultProject);
  }

  return (
    <form className="card form-grid" onSubmit={submit}>
      <h2>Add Project</h2>
      <input name="project_name" placeholder="Project Name" value={form.project_name} onChange={handleChange} required />
      <textarea name="description" placeholder="Description" value={form.description} onChange={handleChange} required />
      <input name="budget" type="number" placeholder="Budget" value={form.budget} onChange={handleChange} required />
      <input name="expected_roi" type="number" step="0.01" placeholder="Expected ROI" value={form.expected_roi} onChange={handleChange} required />
      <select name="risk_level" value={form.risk_level} onChange={handleChange}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      <input name="team_size" type="number" placeholder="Team Size" value={form.team_size} onChange={handleChange} required />
      <input name="technology_stack" placeholder="technology1, technology2" value={form.technology_stack} onChange={handleChange} required />
      <input name="duration" type="number" placeholder="Duration (months)" value={form.duration} onChange={handleChange} required />
      <input name="strategic_alignment_score" type="number" step="0.01" placeholder="Strategic Alignment Score" value={form.strategic_alignment_score} onChange={handleChange} required />
      <select name="status" value={form.status} onChange={handleChange}>
        <option value="proposed">Proposed</option>
        <option value="active">Active</option>
        <option value="on_hold">On Hold</option>
        <option value="completed">Completed</option>
        <option value="retired">Retired</option>
      </select>
      <button className="btn" type="submit" disabled={loading}>
        {loading ? "Saving..." : "Save Project"}
      </button>
    </form>
  );
}
