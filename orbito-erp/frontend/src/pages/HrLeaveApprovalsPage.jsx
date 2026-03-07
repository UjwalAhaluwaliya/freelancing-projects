import { useEffect, useState } from "react";
import api from "../lib/api";

export default function HrLeaveApprovalsPage() {
  const [requests, setRequests] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function loadRequests() {
    try {
      const response = await api.get("/leave");
      setRequests(response.data?.data || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load leave requests");
    }
  }

  useEffect(() => {
    loadRequests();
  }, []);

  async function processLeave(id, action) {
    setError("");
    setSuccess("");
    try {
      await api.put(`/leave/${action}/${id}`);
      setSuccess(`Leave ${action}d successfully.`);
      await loadRequests();
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to update leave request");
    }
  }

  return (
    <section>
      <h2>Leave Approvals</h2>
      <p className="muted">Approve or reject pending employee leaves.</p>
      {error ? <p className="error-text">{error}</p> : null}
      {success ? <p className="success-text">{success}</p> : null}
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Employee</th>
              <th>Type</th>
              <th>Dates</th>
              <th>Days</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((req) => (
              <tr key={req.id}>
                <td>{req.id}</td>
                <td>{req.employee_id}</td>
                <td>{req.leave_type}</td>
                <td>
                  {req.start_date} to {req.end_date}
                </td>
                <td>{req.days_requested}</td>
                <td>{req.status}</td>
                <td>
                  {req.status === "pending" ? (
                    <div className="action-row">
                      <button type="button" onClick={() => processLeave(req.id, "approve")}>
                        Approve
                      </button>
                      <button type="button" onClick={() => processLeave(req.id, "reject")}>
                        Reject
                      </button>
                    </div>
                  ) : (
                    "-"
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
