import { useEffect, useState } from "react";
import api from "../lib/api";

export default function HrInterviewsPage() {
  const [interviews, setInterviews] = useState([]);
  const [applications, setApplications] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [form, setForm] = useState({
    application_id: "",
    interviewer_name: "",
    interview_date: "",
  });

  async function loadData() {
    try {
      const [interviewsRes, appsRes] = await Promise.all([
        api.get("/interviews"),
        api.get("/applications"),
      ]);
      setInterviews(interviewsRes.data?.data || []);
      setApplications(appsRes.data?.data || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load interview data");
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function scheduleInterview(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    try {
      await api.post("/interviews", {
        application_id: form.application_id,
        interviewer_name: form.interviewer_name,
        interview_date: new Date(form.interview_date).toISOString(),
      });
      setForm({ application_id: "", interviewer_name: "", interview_date: "" });
      setSuccess("Interview scheduled.");
      await loadData();
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to schedule interview");
    }
  }

  async function markCompleted(interviewId) {
    setError("");
    setSuccess("");
    try {
      await api.put(`/interviews/${interviewId}`, {
        status: "completed",
      });
      setSuccess("Interview marked as completed.");
      await loadData();
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to update interview");
    }
  }

  return (
    <section>
      <h2>Interview Management</h2>
      <p className="muted">Schedule and update candidate interviews.</p>
      {error ? <p className="error-text">{error}</p> : null}
      {success ? <p className="success-text">{success}</p> : null}

      <div className="split-grid">
        <form className="card form-card" onSubmit={scheduleInterview}>
          <h3>Schedule Interview</h3>
          <select
            value={form.application_id}
            onChange={(event) => setForm({ ...form, application_id: event.target.value })}
            required
          >
            <option value="">Select application</option>
            {applications.map((app) => (
              <option key={app.id} value={app.id}>
                {app.id} ({app.stage})
              </option>
            ))}
          </select>
          <input
            placeholder="Interviewer name"
            value={form.interviewer_name}
            onChange={(event) => setForm({ ...form, interviewer_name: event.target.value })}
            required
          />
          <input
            type="datetime-local"
            value={form.interview_date}
            onChange={(event) => setForm({ ...form, interview_date: event.target.value })}
            required
          />
          <button type="submit">Schedule</button>
        </form>

        <div className="table-wrap">
          <div className="filter-row">
            <h3>Interviews</h3>
          </div>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Application</th>
                <th>Interviewer</th>
                <th>Date</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {interviews.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.application_id}</td>
                  <td>{item.interviewer_name}</td>
                  <td>{new Date(item.interview_date).toLocaleString()}</td>
                  <td>{item.status}</td>
                  <td>
                    {item.status !== "completed" ? (
                      <button type="button" onClick={() => markCompleted(item.id)}>
                        Mark Completed
                      </button>
                    ) : (
                      "-"
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
