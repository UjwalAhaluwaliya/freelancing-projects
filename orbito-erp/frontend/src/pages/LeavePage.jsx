import { useEffect, useState } from "react";
import api from "../lib/api";
import { decodeToken, getToken } from "../lib/auth";

export default function LeavePage() {
  const [form, setForm] = useState({
    leave_type: "casual",
    start_date: "",
    end_date: "",
    reason: "",
  });
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [myLeaves, setMyLeaves] = useState([]);

  async function loadMyLeaves() {
    try {
      const response = await api.get("/leave/my");
      setMyLeaves(response.data?.data || []);
    } catch {
      setMyLeaves([]);
    }
  }

  useEffect(() => {
    loadMyLeaves();
  }, []);

  async function submitLeave(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult("");
    try {
      const tokenPayload = decodeToken(getToken() || "");
      const employeeId = tokenPayload?.user_id;
      if (!employeeId) {
        throw new Error("Unable to identify logged-in user");
      }
      await api.post("/leave", { ...form, employee_id: employeeId });
      setResult("Leave request submitted successfully.");
      setForm({ ...form, start_date: "", end_date: "", reason: "" });
      await loadMyLeaves();
    } catch (err) {
      setError(err?.response?.data?.detail || err.message || "Leave request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h2>Apply Leave</h2>
      <p className="muted">Submit leave request with date validation.</p>
      <form className="card form-card narrow" onSubmit={submitLeave}>
        <label htmlFor="leaveType">Leave Type</label>
        <select
          id="leaveType"
          value={form.leave_type}
          onChange={(event) => setForm({ ...form, leave_type: event.target.value })}
        >
          <option value="casual">Casual</option>
          <option value="sick">Sick</option>
          <option value="earned">Earned</option>
        </select>
        <label htmlFor="startDate">Start Date</label>
        <input
          id="startDate"
          type="date"
          value={form.start_date}
          onChange={(event) => setForm({ ...form, start_date: event.target.value })}
          required
        />
        <label htmlFor="endDate">End Date</label>
        <input
          id="endDate"
          type="date"
          value={form.end_date}
          onChange={(event) => setForm({ ...form, end_date: event.target.value })}
          required
        />
        <label htmlFor="reason">Reason</label>
        <textarea
          id="reason"
          value={form.reason}
          onChange={(event) => setForm({ ...form, reason: event.target.value })}
          required
        />
        {error ? <p className="error-text">{error}</p> : null}
        {result ? <p className="success-text">{result}</p> : null}
        <button type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Submit Leave"}
        </button>
      </form>
      <div className="table-wrap">
        <div className="filter-row">
          <h3>My Leave Requests</h3>
          <button type="button" onClick={loadMyLeaves}>
            Refresh
          </button>
        </div>
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>Start</th>
              <th>End</th>
              <th>Days</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {myLeaves.map((item) => (
              <tr key={item.id}>
                <td>{item.leave_type}</td>
                <td>{item.start_date}</td>
                <td>{item.end_date}</td>
                <td>{item.days_requested}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
